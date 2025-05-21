import streamlit as st # type: ignore # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import plotly.express as px # type: ignore
from datetime import datetime, timedelta
from fpdf import FPDF # type: ignore
import tempfile
import os

st.set_page_config(page_title="WORKSAFE PRO - Dashboard HSE", layout="wide")
st.title("🏭 WORKSAFE PRO - Dashboard Sicurezza Aziendale")

st.markdown("""
Questa dashboard monitora in tempo reale parametri ergonomici e di sicurezza per il personale operativo:
- Movimenti a rischio
- Tempo in postura scorretta
- Forza lombare stimata
- Indice ergonomico complessivo
- Frequenza di feedback correttivi
- Eventi critici segnalati
- Reportistica conforme alle normative HSE
""")

# Simulazione dati ultimi 30 giorni
oggi = datetime.now()
dati = {
    "Data": [(oggi - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)],
    "Movimenti a rischio": np.random.randint(0, 5, 30),
    "Tempo in postura scorretta (min)": np.random.normal(20, 8, 30).round(1),
    "Forza zona lombare (kg)": np.random.normal(16, 4, 30).round(1),
    "Indice ergonomico": np.random.normal(72, 10, 30).round(1),
    "Feedback correttivi": np.random.randint(0, 4, 30),
    "Eventi critici segnalati": np.random.randint(0, 2, 30)
}
df = pd.DataFrame(dati)

# KPI
st.subheader("📊 Indicatori Chiave di Sicurezza")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Movimenti a rischio totali", int(df['Movimenti a rischio'].sum()))
kpi2.metric("Postura scorretta media (min)", f"{df['Tempo in postura scorretta (min)'].mean():.1f}")
kpi3.metric("Indice ergonomico medio", f"{df['Indice ergonomico'].mean():.1f}")

# Grafici
st.subheader("📈 Analisi delle ultime 4 settimane")
tabs = st.tabs(["Trend", "Distribuzione", "Tabella Dati"])

with tabs[0]:
    fig = px.line(df, x="Data", y=["Movimenti a rischio", "Indice ergonomico"], markers=True, title="Trend Sicurezza")
    st.plotly_chart(fig, use_container_width=True)
    fig2 = px.area(df, x="Data", y="Tempo in postura scorretta (min)", title="Tempo in postura scorretta")
    st.plotly_chart(fig2, use_container_width=True)

with tabs[1]:
    fig3 = px.histogram(df, x="Forza zona lombare (kg)", nbins=20, title="Distribuzione Forza su zona lombare")
    st.plotly_chart(fig3, use_container_width=True)

with tabs[2]:
    st.dataframe(df.tail(10))
    st.download_button("📥 Scarica tutti i dati (CSV)", df.to_csv(index=False).encode('utf-8'), file_name="report_hse.csv")

# Generazione PDF semplificata
def crea_pdf_hse(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "WORKSAFE PRO - Report Sicurezza", ln=True, align='C')
    pdf.set_font("Arial", '', 11)
    pdf.ln(5)
    pdf.multi_cell(0, 10, "Report settimanale conforme alle linee guida HSE. Include analisi sintetica dei rischi e KPI ergonomici.")
    pdf.ln(5)
    for i, row in data.tail(5).iterrows():
        pdf.cell(200, 10, f"{row['Data']}: Rischi={row['Movimenti a rischio']}, Postura={row['Tempo in postura scorretta (min)']} min, Indice={row['Indice ergonomico']}, Feedback={row['Feedback correttivi']}, Eventi Critici={row['Eventi critici segnalati']}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, "Generato automaticamente per finalità di compliance HSE.", ln=True, align='L')
    path = os.path.join(tempfile.gettempdir(), "report_hse.pdf")
    pdf.output(path)
    return path

st.subheader("📄 Esportazione Reportistica per Compliance HSE")
if st.button("Genera PDF Report Conforme"):
    pdf_path = crea_pdf_hse(df)
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Scarica PDF", f, file_name="report_hse.pdf", mime="application/pdf")
