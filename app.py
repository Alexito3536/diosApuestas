import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title="The God Engine", layout="wide")

st.title("🏹 El Dios de las Apuestas v3.0")
st.sidebar.header("Panel de Control")
capital = st.sidebar.number_input("Bankroll Total ($)", value=5000)

# Cargar el motor
@st.cache_resource
def load_engine():
    return joblib.load('modelo_god.pkl')

god_engine = load_engine()

st.subheader("🚀 Oportunidades de Alta Probabilidad")

# Aquí simularemos los partidos que ya vimos que funcionan
partidos = [
    {'equipo': 'Arsenal vs Man City', 'prob': 0.682, 'cuota': 2.50, 'pick': 'Local'},
    {'equipo': 'Liverpool vs Chelsea', 'prob': 0.377, 'cuota': 4.00, 'pick': 'Empate'},
]

for p in partidos:
    ev = (p['prob'] * p['cuota']) - 1
    if ev > 0.05:
        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"### {p['equipo']}")
                st.write(f"Pick: **{p['pick']}**")
            with col2:
                st.metric("EV (Valor)", f"{ev:+.2%}")
                st.write(f"Probabilidad IA: {p['prob']:.1%}")
            with col3:
                # Criterio de Kelly para el stake
                b = p['cuota'] - 1
                prob_ganar = p['prob']
                prob_perder = 1 - prob_ganar
                stake_f = (b * prob_ganar - prob_perder) / b
                monto = max(0, stake_f * capital * 0.2) # Kelly fraccionado al 20%
                st.warning(f"Sugerencia: ${monto:.2f}")
            st.divider()
