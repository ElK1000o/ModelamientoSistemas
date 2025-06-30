import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

st.set_page_config(page_title="Intervención sobre desplazamiento", layout="wide")
st.markdown("<h1 style='text-align: center; font-size: 2.5em;'>Intervención y Desplazamiento</h1>", unsafe_allow_html=True)

# Variables base
variables = [
    "Inversión inmobiliaria", "Especulación inmobiliaria", "Turistificación",
    "Costo habitacional", "Accesibilidad vivienda",
    "Políticas renovación", "Protección patrimonial",
    "Incentivos economía local", "Participación ciudadana",
    "Identidad barrial"
]

# Índices de variables intervenibles
indices_intervenibles = [4, 5, 6, 7, 8]  # Accesibilidad vivienda, Políticas renovación, etc.

# MATRIZ 11x11
A_11 = np.array([
    [-3,  0,  0,  1,  0,  0,  0,  0,  0,  0,  1], # Inversión inmobiliaria
    [ 0, -3,  0,  1,  0,  0,  0,  0,  0,  0,  0], # Especulación inmobiliaria
    [ 1,  0, -3,  0,  0,  0,  0,  0,  0,  0,  1], # Turistificación
    [ 0,  0,  0, -3, -1,  0,  0,  0, -1,  0,  0], # Costo habitacional
    [ 0,  0,  0,  0, -3,  0,  0,  0,  0,  0, -1], # Accesibilidad a la vivienda *
    [ 1,  0,  0,  1,  1, -3,  0,  0,  0,  0, -1], # Políticas de renovación urbana *
    [-1,  0,  0,  0,  0,  0, -3,  0,  1,  1, -1], # Protección patrimonial participativa *
    [ 0,  0,  0,  0,  0,  0,  0, -3,  1,  1, -1], # Incentivos a la economía local *
    [ 0,  0,  0,  0,  0,  0,  1,  1, -3,  1,  0], # Participación ciudadana *
    [ 0,  0,  0,  0 , 0,  0,  0,  0,  0, -3, -1], # Identidad barrial
    [ 0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -3], # Desplazamiento ***
 ], dtype=float)

# MATRIZ 12x12 (base editable)
A_12 = np.array([
    [-3,  0,  0,  1,  0,  0,  0,  0,  0,  0,  1,  0], # Inversión inmobiliaria
    [ 0, -3,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0], # Especulación inmobiliaria
    [ 1,  0, -3,  0,  0,  0,  0,  0,  0,  0,  1,  0], # Turistificación
    [ 0,  0,  0, -3, -1,  0,  0,  0, -1,  0,  0,  0], # Costo habitacional
    [ 0,  0,  0,  0, -3,  0,  0,  0,  0,  0, -1,  -1], # Accesibilidad a la vivienda *
    [ 1,  0,  0,  1,  1, -3,  0,  0,  0,  0, -1,  -1], # Políticas de renovación urbana *
    [-1,  0,  0,  0,  0,  0, -3,  0,  1,  1, -1,  -1], # Protección patrimonial participativa *
    [ 0,  0,  0,  0,  0,  0,  0, -3,  1,  1, -1,  -1], # Incentivos a la economía local *
    [ 0,  0,  0,  0,  0,  0,  1,  1, -3,  1,  0,  -1], # Participación ciudadana *
    [ 0,  0,  0,  0 , 0,  0,  0,  0,  0, -3, -1,  0], # Identidad barrial
    [ 0,  0,  0,  0,  0,  0,  0,  0, -1, -1, -3,  0], # Desplazamiento ***
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, -3], # 
], dtype=float)

# --- Sliders para ajustar fila 12 (solo intervenciones permitidas) ---
st.sidebar.header("Ajuste de intervención externa")
intervencion = []
for i in range(len(variables)):
    if i in indices_intervenibles:
        valor = st.sidebar.slider(f"{variables[i]}", -3.0, 3.0, float(A_12[i, 11]), step=0.1)
        A_12[i, 11] = valor
        intervencion.append(valor)
    else:
        intervencion.append(float(A_12[i, 11]))  # mantener sin cambios

# Inversas negativas
Ainv_11 = inv(-A_11)
Ainv_12 = inv(-A_12)

# Efectos sobre desplazamiento
efecto_11x11 = Ainv_11[:, 10]
efecto_12x12 = Ainv_12[:11, 11]
efecto_11x11 = efecto_11x11[:-1]
efecto_12x12 = efecto_12x12 [:-1]

# --- Gráfico ---
fig, ax = plt.subplots(1, 2, figsize=(18, 7), sharey=True)

ax[0].barh(variables, efecto_11x11, color="royalblue")
ax[0].set_title("Impacto neto sobre Desplazamiento (11x11)")
ax[0].set_xlabel("Magnitud del efecto")
ax[0].invert_yaxis()

ax[1].barh(variables, efecto_12x12, color="tomato")
ax[1].set_title("Impacto con Intervención Externa (12x12)")
ax[1].set_xlabel("Magnitud del efecto")
ax[1].invert_yaxis()

st.pyplot(fig)

# --- Mostrar la matriz modificada (opcional) ---
with st.expander("Ver fila de intervención aplicada"):
    st.write(dict(zip(variables, intervencion)))
