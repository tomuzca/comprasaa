import streamlit as st
import pandas as pd
from joblib import load
import numpy as np

# Cargar el modelo entrenado
model = load("../src/random_forest_regressor_default_42.pkl")

regiones = ["DEL BIOBIO","METROPOLITANA DE SANTIAGO",
            "DE VALPARAISO", "DEL MAULE", "DE LA ARAUCANIA", 
            "DE ÑUBLE", "DEL LIBERTADOR GENERAL BERNARDO O'HIGGINS",
            "DE COQUIMBO", "DE ATACAMA", "DE ANTOFAGASTA",
            "DE LOS LAGOS", "DE LOS RIOS", "DE PAINE", "DE ARICA Y PARINACOTA"]

st.title("Primer estimador fletes $ x Kg")

pesototal = st.slider('Ingrese el peso', min_value=5000, max_value=30000)

region = st.selectbox("Ingrese la región", regiones)

if st.button("Calcular"):
    # Crear un vector con el peso y el one-hot encoding de la región
    regiones_oh = np.zeros(len(regiones))
    regiones_oh[regiones.index(region)] = 1

    vector_pred =[ int(pesototal)] + list(regiones_oh)

    # Realizar la predicción
    prediction = model.predict([vector_pred])[0]
    st.write("El estimado del flete es de", prediction)
