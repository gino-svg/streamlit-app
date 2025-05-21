import streamlit as st # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import plotly.express as px # type: ignore
from datetime import datetime, timedelta
from fpdf import FPDF # type: ignore
import tempfile
import os

st.set_page_config(page_title="MOVE Coach Toolkit App", layout="wide")
st.title("🎯 M.O.V.E. - Coach Toolkit App")

st.markdown("""
Questa applicazione permette ad allenatori, preparatori e fisioterapisti di:
- Caricare sessioni di allenamento
- Analizzare postura, simmetria, andatura, frequenza cardiaca
- Ricevere alert su movimenti a rischio
- Confrontare sessioni
- Esportare dati in CSV e PDF
""")

# Simulazione dati biometrici
def genera_sessione(nome_sessione, giorni=1):
    date_range = [datetime.now() - timedelta(days=i) for i in range(giorni)]
    data = {
        "Data": date_range,
        "Postura Score": np.random.normal(75, 5, giorni),
        "Simmetria (%)": np.random.normal(85, 7, giorni),
        "Andatura Score": np.random.normal(80, 6, giorni),
        "Movimenti a rischio": np.random.randint(0, 3, giorni),
        "Frequenza cardiaca": np.random.normal(120, 10, giorni)
    }
    return pd.DataFrame(data)

# Sessioni simulate
sessioni = {
    "Sessione 1": genera_sessione("Sessione 1", 10),
    "Sessione 2": genera_sessione("Sessione 2", 10),
    "Sessione 3": genera_sessione("Sessione 3", 10)
}

sessione_scelta = st.selectbox("📂 Seleziona una sessione di allenamento", list(sessioni.keys()))
df = sessioni[sessione_scelta]

st.subheader("📊 Analisi Biomeccanica")
col1, col2 = st.columns(2)
with col1:
    st.metric("Postura media", f"{df['Postura Score'].mean():.1f}")
    st.metric("Simmetria media", f"{df['Simmetria (%)'].mean():.1f}%")
with col2:
    st.metric("Andatura media", f"{df['Andatura Score'].mean():.1f}")
    st.metric("Movimenti a rischio", int(df['Movimenti a rischio'].sum()))

# Grafici dinamici
st.plotly_chart(px.line(df, x="Data", y=["Postura Score", "Simmetria (%)", "Andatura Score"], markers=True), use_container_width=True)
st.plotly_chart(px.bar(df, x="Data", y="Frequenza cardiaca", title="Frequenza Cardiaca"), use_container_width=True)

# Alert visivo
if df['Movimenti a rischio'].sum() > 0:
    st.warning("⚠️ Sono stati rilevati movimenti a rischio durante la sessione")

st.subheader("📋 Dati dettagliati")
st.dataframe(df)

# Confronto sessioni
st.subheader("📈 Confronto tra sessioni")
scelte = st.multiselect("Seleziona sessioni da confrontare", list(sessioni.keys()), default=["Sessione 1", "Sessione 2"])
if len(scelte) > 1:
    confronto_df = pd.concat([sessioni[s].assign(Sessione=s) for s in scelte])
    st.plotly_chart(px.box(confronto_df, x="Sessione", y="Postura Score", title="Confronto Postura"))
    st.plotly_chart(px.box(confronto_df, x="Sessione", y="Simmetria (%)", title="Confronto Simmetria"))
    st.plotly_chart(px.box(confronto_df, x="Sessione", y="Andatura Score", title="Confronto Andatura"))

# Esportazione CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Scarica dati sessione (CSV)", csv, f"report_{sessione_scelta.lower().replace(' ', '_')}.csv", "text/csv")

# Esportazione PDF
def genera_pdf(nome, dati):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Report - {nome}", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Data generazione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    for i, row in dati.head(5).iterrows():
        pdf.cell(200, 10, f"{row['Data'].strftime('%Y-%m-%d')}: Postura={row['Postura Score']:.1f}, Simmetria={row['Simmetria (%)']:.1f}, Andatura={row['Andatura Score']:.1f}, FC={row['Frequenza cardiaca']:.1f}, Rischi={row['Movimenti a rischio']}", ln=True)
    temp_path = os.path.join(tempfile.gettempdir(), f"report_{nome}.pdf")
    pdf.output(temp_path)
    return temp_path

if st.button("📄 Genera PDF della sessione"):
    path_pdf = genera_pdf(sessione_scelta, df)
    with open(path_pdf, "rb") as f:
        st.download_button("📥 Scarica PDF", f, file_name=os.path.basename(path_pdf), mime="application/pdf")
