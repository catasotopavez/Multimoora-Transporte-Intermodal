
import streamlit as st
import pandas as pd
from io import StringIO
from utils.utils import load_and_clean_csv, run_multimoora
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="3. Análisis MULTIMOORA", layout="wide")
st.title("📊 3. Análisis MULTIMOORA")

st.markdown("Sube tres archivos CSV con los resultados de cada función objetivo:")

file_min_costos = st.file_uploader("🔹 MIN COSTOS", type="csv")
file_max_entropia = st.file_uploader("🔹 MAX ENTROPÍA", type="csv")
file_min_var_costos = st.file_uploader("🔹 MIN VAR COSTOS", type="csv")

st.markdown("### ⚖️ Define los pesos para cada criterio (deben sumar 1.0):")
col1, col2, col3, col4 = st.columns(4)
peso_z = col1.number_input("Peso Z", min_value=0.0, max_value=1.0, value=0.25)
peso_ent = col2.number_input("Peso ENT", min_value=0.0, max_value=1.0, value=0.25)
peso_var = col3.number_input("Peso VAR", min_value=0.0, max_value=1.0, value=0.25)
peso_lambda = col4.number_input("Peso Lambda", min_value=0.0, max_value=1.0, value=0.25)

procesar = st.button("🚀 Procesar MULTIMOORA")

if procesar:
    if not all([file_min_costos, file_max_entropia, file_min_var_costos]):
        st.error("❌ Debes subir los tres archivos CSV.")
    elif round(peso_z + peso_ent + peso_var + peso_lambda, 5) != 1.0:
        st.error("⚠️ La suma de los pesos debe ser exactamente 1.0")
    else:
        # Cargar archivos
        df1 = load_and_clean_csv(StringIO(file_min_costos.getvalue().decode()), "Min Costos")
        df2 = load_and_clean_csv(StringIO(file_max_entropia.getvalue().decode()), "Max Entropía")
        df3 = load_and_clean_csv(StringIO(file_min_var_costos.getvalue().decode()), "Min Varianza")
        df_combined = pd.concat([df1, df2, df3], ignore_index=True)

        weights = {'Z': peso_z, 'ENT': peso_ent, 'VAR': peso_var, 'Lambda': peso_lambda}
        df_normalized, df_resultado = run_multimoora(df_combined, weights)

        st.subheader("📘 Matriz Original")
        st.dataframe(df_combined)

        st.subheader("📗 Matriz Normalizada")
        st.dataframe(df_normalized)

        st.subheader("📙 Matriz Ponderada")
        st.dataframe(df_resultado[['Objetivo', 'Lambda_val', 'Z', 'ENT', 'VAR', 'Lambda']])

        st.markdown("---")
        st.markdown("## 🔍 Paso a paso de los métodos MULTIMOORA")

        with st.expander("📈 Método 1: Ratio System (RS)"):
            st.write("Se calcula la suma ponderada de todos los criterios:")
            st.code("RatioSystem = Z + ENT + VAR + Lambda")
            st.dataframe(df_resultado[['Objetivo', 'Lambda_val', 'RatioSystem', 'Rank_RS']])

        with st.expander("📏 Método 2: Reference Point (RP)"):
            st.write("Se calcula la desviación máxima respecto al valor ideal para cada criterio:")
            st.code("ReferencePoint = max(|ideal - valor_criterio|)")
            st.dataframe(df_resultado[['Objetivo', 'Lambda_val', 'ReferencePoint', 'Rank_RP']])

        with st.expander("📊 Método 3: Full Multiplicative Form (FMF)"):
            st.write("Se calcula el producto ponderado de todos los criterios normalizados:")
            st.code("FMF = Z^wZ * ENT^wENT * VAR^wVAR * Lambda^wLambda")
            st.dataframe(df_resultado[['Objetivo', 'Lambda_val', 'FMF', 'Rank_FMF']])

        st.markdown("---")
        st.subheader("🏁 Ranking Final")
        st.dataframe(df_resultado.sort_values('Ranking_Final_Suma')[
            ['Objetivo', 'Lambda_val', 'Rank_RS', 'Rank_RP', 'Rank_FMF',
             'Ranking_Suma', 'Ranking_Final_Suma', 'Ranking_Promedio', 'Ranking_Final_Promedio']
        ])
        st.markdown("---")
        st.subheader("📊 Comparación visual: Top 3 soluciones (Gráfico de Radar)")

        import plotly.graph_objects as go

        # Criterios en el orden solicitado
        criterios = ["Lambda", "Z", "ENT", "VAR"]

        # Obtener los índices del top 3 según Ranking_Final_Suma
        top3_idx = df_resultado.sort_values("Ranking_Final_Suma").head(3).index

        # Tomar esas filas desde la matriz normalizada
        fig = go.Figure()
        max_val = df_normalized[criterios].max().max()

        for idx in top3_idx:
            fila = df_normalized.loc[idx]
            nombre = f"{df_resultado.loc[idx, 'Objetivo']} (λ={df_resultado.loc[idx, 'Lambda_val']})"
            fig.add_trace(go.Scatterpolar(
                r=[fila[c] for c in criterios],
                theta=criterios,
                fill='toself',
                name=nombre
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, round(max_val + 0.05, 1)],
                    tickmode='linear',
                    dtick=0.1
                )
            ),
            showlegend=True,
            title="Radar de criterios normalizados (Lambda, Z, ENT, VAR) - Top 3 soluciones"
        )

        st.plotly_chart(fig, use_container_width=True)
