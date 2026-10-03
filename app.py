import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Tamizaje Cardiopatías Congénitas Fetales",
    page_icon="🫀",
    layout="wide",
)

HALLAZGOS = {
    "corte_4c_anormal":         (3, "Corte de 4 cámaras anormal"),
    "tracto_salida_anormal":    (3, "Tractos de salida anormales"),
    "eje_cardiaco_anormal":     (2, "Eje cardíaco anormal"),
    "derrame_pericardico":      (2, "Derrame pericárdico"),
    "ritmo_anormal":            (2, "Arritmia fetal"),
    "tn_aumentada":             (2, "Translucencia nucal aumentada"),
    "ductus_venoso_anormal":    (2, "Ductus venoso con onda a reversa"),
    "regurgitacion_tricuspide": (2, "Regurgitación tricuspídea significativa"),
    "arteria_umbilical_unica":  (1, "Arteria umbilical única"),
    "antecedente_familiar":     (2, "Antecedente familiar de cardiopatía"),
    "diabetes_materna":         (1, "Diabetes materna pregestacional"),
    "lupus_anti_ro":            (2, "Lupus / anti-Ro positivo"),
    "foco_ecogenico":           (1, "Foco ecogénico intracardíaco"),
}

def evaluar(hallazgos):
    score = 0
    positivos = []
    for clave, valor in hallazgos.items():
        if valor:
            peso, desc = HALLAZGOS[clave]
            score += peso
            positivos.append(desc)

    if score == 0:
        nivel, color = "Riesgo bajo", "green"
    elif score <= 3:
        nivel, color = "Riesgo intermedio", "orange"
    elif score <= 7:
        nivel, color = "Riesgo alto", "red"
    else:
        nivel, color = "Riesgo muy alto", "darkred"

    return score, nivel, color, positivos


st.title("🫀 Tamizaje de Cardiopatías Congénitas Fetales")
st.caption("Semana 20 · Herramienta educativa de apoyo")
st.warning(
    "⚠️ Esta app es **educativa**. No reemplaza el juicio clínico "
    "ni el ecocardiograma fetal por especialista."
)

with st.sidebar:
    st.header("Datos de la gestación")
    st.number_input("Edad materna", 15, 55, 30)
    st.number_input("Edad gestacional (semanas)", 18, 24, 20)
    st.divider()
    st.header("Hallazgos ecográficos")
    hallazgos = {}
    for clave, (peso, desc) in HALLAZGOS.items():
        hallazgos[clave] = st.checkbox(desc)

score, nivel, color, positivos = evaluar(hallazgos)

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Puntaje de riesgo", score)
    st.markdown(f"<h3>● {nivel}</h3>", unsafe_allow_html=True)

with col2:
    if positivos:
        st.subheader("Hallazgos positivos")
        for h in positivos:
            st.write(f"- {h}")
    else:
        st.success("No se registraron hallazgos de riesgo.")

st.divider()
st.subheader("Recomendaciones orientativas")

if score == 0:
    st.info("Continuar con control prenatal habitual. Tamizaje ecográfico de rutina.")
elif score <= 3:
    st.info("Considerar ecografía dirigida y seguimiento. Reevaluar en 4 semanas.")
elif score <= 7:
    st.warning("Derivar a ecocardiograma fetal por cardiología pediátrica.")
else:
    st.error("Derivación URGENTE a ecocardiograma fetal. Manejo multidisciplinario.")
