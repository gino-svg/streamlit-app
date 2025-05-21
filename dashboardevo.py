import streamlit as st # type: ignore
import pandas as pd # type: ignore # type: ignore
import numpy as np # type: ignore
from datetime import datetime, timedelta
import plotly.express as px # type: ignore

st.set_page_config(page_title="Dashboard Move Evo", layout="wide")
st.title("🦾 Dashboard Sanitaria - Analisi Movimento")

# Generazione dati simulati
oggi = datetime.now()
dati = {
    "Data": [(oggi - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(30)],
    "Postura Score": np.random.normal(75, 7, 30).round(2),
    "Simmetria (%)": np.random.normal(90, 5, 30).round(2),
    "Andatura Score": np.random.normal(85, 6, 30).round(2),
    "Movimenti a rischio": np.random.randint(0, 4, 30),
    "Equilibrio Dinamico": np.random.normal(80, 8, 30).round(2),
    "Stabilità Posturale": np.random.normal(78, 6, 30).round(2),
    "Variazione Passi (%)": np.random.normal(5, 2, 30).round(2)
}
df = pd.DataFrame(dati)

# KPI
st.subheader("Indicatori Clinici")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Postura Media", f"{df['Postura Score'].mean():.1f}")
kpi2.metric("Simmetria Media", f"{df['Simmetria (%)'].mean():.1f}%")
kpi3.metric("Andatura Media", f"{df['Andatura Score'].mean():.1f}")
kpi4.metric("Movimenti a rischio/giorno", f"{df['Movimenti a rischio'].mean():.2f}")

# Grafici
st.subheader("Trend degli Ultimi 30 Giorni")
tab1, tab2, tab3 = st.tabs(["📉 Andamento Score", "📊 Equilibrio e Stabilità", "📁 Tabella Dati"])

with tab1:
    fig1 = px.line(df.sort_values(by="Data"), x="Data", y=["Postura Score", "Andatura Score"], 
                  markers=True, labels={"value": "Score", "variable": "Parametro"}, 
                  title="Andamento Postura e Andatura")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.bar(df.sort_values(by="Data"), x="Data", y=["Equilibrio Dinamico", "Stabilità Posturale"], 
                 barmode="group", title="Equilibrio Dinamico e Stabilità Posturale")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.dataframe(df.tail(10), use_container_width=True)
    st.download_button("Scarica Tutti i Dati", df.to_csv(index=False).encode('utf-8'), file_name="report_move.csv")
