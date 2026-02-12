import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np

# 1. Configuración de la Interfaz
st.set_page_config(page_title="El Dios de las Apuestas v3.0", page_icon="🏹", layout="wide")

st.title("🏹 El Dios de las Apuestas v3.0")
st.markdown("---")

# 2. Función Maestra de Carga (Solución al AttributeError)
@st.cache_resource
def load_engine():
    model_path = 'modelo_god.pkl'
    if not os.path.exists(model_path):
        st.error(f"❌ No se encontró el archivo '{model_path}' en GitHub.")
        return None
    
    try:
        data = joblib.load(model_path)
        # Verificamos si lo que cargamos es la clase completa o solo el modelo
        if hasattr(data, 'model'):
            return data.model
        return data
    except Exception as e:
        st.error(f"❌ Error al procesar el cerebro: {e}")
        return None

# Ejecutar carga
model = load_engine()

# 3. Panel de Control Lateral
st.sidebar.header("💰 Gestión de Bankroll")
bankroll = st.sidebar.number_input("Tu Capital Total ($)", value=5000)
min_ev = st.sidebar.slider("Umbral de Valor (Min EV %)", 0, 50, 10) / 100

if model:
    st.sidebar.success("✅ Oráculo Conectado")
    
    # 4. Simulación de Análisis de Partidos (Aquí es donde ocurre la magia)
    st.subheader("🚀 Oportunidades con Ventaja Matemática (+EV)")
    
    # Datos de prueba basados en tus resultados de Colab
    # En el futuro, aquí conectaremos el Scraper automático
    proximos_partidos = [
        {'equipo': 'Arsenal vs Man City', 'prob_h': 0.682, 'cuota_h': 2.50, 'pick': 'Local (Arsenal)'},
        {'equipo': 'Liverpool vs Chelsea', 'prob_h': 0.538, 'cuota_h': 1.90, 'pick': 'Local (Liverpool)'},
        {'equipo': 'Man United vs Tottenham', 'prob_h': 0.696, 'cuota_h': 2.10, 'pick': 'Local (Man Utd)'}
    ]

    cols = st.columns(len(proximos_partidos))

    for i, juego in enumerate(proximos_partidos):
        with cols[i]:
            # Cálculo de Valor Esperado (EV)
            ev = (juego['prob_h'] * juego['cuota_h']) - 1
            
            st.markdown(f"### {juego['equipo']}")
            
            if ev >= min_ev:
                st.write(f"🎯 **Pick Sugerido:** {juego['pick']}")
                st.metric("EV Detectado", f"{ev:+.2%}")
                
                # Gestión de Riesgo (Criterio de Kelly al 20%)
                b = juego['cuota_h'] - 1
                p = juego['prob_h']
                q = 1 - p
                kelly = (b * p - q) / b
                apuesta_sugerida = max(0, kelly * bankroll * 0.2)
                
                st.success(f"💸 Apostar: ${apuesta_sugerida:.2f}")
            else:
                st.info("Buscando valor...")
            st.divider()

    st.write("💡 *El modelo analiza variables de rendimiento, agresividad y efectividad de tiros.*")

else:
    st.warning("⚠️ Esperando conexión con el modelo para iniciar el análisis...")
