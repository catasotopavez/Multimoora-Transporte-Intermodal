
import streamlit as st
import pandas as pd
from io import StringIO
from utils.utils import load_and_clean_csv, normalize_criteria, run_multimoora

st.set_page_config(page_title="MULTIMOORA Interactivo", layout="wide")
st.title("Análisis MULTIMOORA")

st.markdown("Sube tres archivos CSV con los resultados de cada función objetivo:")

# Subida de archivos
file_min_costos = st.file_uploader("🔹 MIN COSTOS", type="csv")
file_max_entropia = st.file_uploader("🔹 MAX ENTROPÍA", type="csv")
file_min_var_costos = st.file_uploader("🔹 MIN VAR COSTOS", type="csv")

st.markdown("### ⚖️ Define los pesos para cada criterio (deben sumar 1.0):")
col1, col2, col3, col4 = st.columns(4)
peso_z = col1.number_input("Peso Z", min_value=0.0, max_value=1.0, value=0.25)
peso_ent = col2.number_input("Peso ENT", min_value=0.0, max_value=1.0, value=0.25)
peso_var = col3.number_input("Peso VAR", min_value=0.0, max_value=1.0, value=0.25)
peso_lambda = col4.number_input("Peso Lambda", min_value=0.0, max_value=1.0, value=0.25)

procesar = st.button("Procesar MULTIMOORA")

if procesar:
    if not all([file_min_costos, file_max_entropia, file_min_var_costos]):
        st.error("⚠️ Debes subir los tres archivos CSV.")
    elif round(peso_z + peso_ent + peso_var + peso_lambda, 5) != 1.0:
        st.error("⚠️ La suma de los pesos debe ser exactamente 1.0")
    else:
        # Leer archivos
        df1 = load_and_clean_csv(StringIO(file_min_costos.getvalue().decode()), "Min Costos")
        df2 = load_and_clean_csv(StringIO(file_max_entropia.getvalue().decode()), "Max Entropía")
        df3 = load_and_clean_csv(StringIO(file_min_var_costos.getvalue().decode()), "Min Varianza")

        df_combined = pd.concat([df1, df2, df3], ignore_index=True)

        # Definir pesos personalizados
        weights = {'Z': peso_z, 'ENT': peso_ent, 'VAR': peso_var, 'Lambda': peso_lambda}

        # Ejecutar MULTIMOORA
        df_normalized, df_resultado = run_multimoora(df_combined, weights)

        st.subheader("📘 Matriz Original")
        st.dataframe(df_combined)

        st.subheader("📗 Matriz Normalizada")
        st.dataframe(df_normalized)

        st.subheader("📙 Matriz Ponderada + Rankings")
        st.dataframe(df_resultado)

        st.subheader("🔸 Ranking Final")
        st.dataframe(df_resultado.sort_values('Ranking_Final_Suma')[
            ['Objetivo', 'Lambda_val', 'Ranking_Final_Suma', 'Ranking_Final_Promedio']
        ])
