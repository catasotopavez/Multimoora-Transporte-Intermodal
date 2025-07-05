import streamlit as st
import pandas as pd
import zipfile
import io
import os


st.set_page_config(page_title="2. GAMS TO CSV", layout="wide")
st.title("🛠️ 2. Transformador GAMS ➜ CSV")

st.markdown("Sube un archivo `.zip` con los Excel de las corridas:")

uploaded_zip = st.file_uploader("Archivo ZIP con resultados de GAMS", type="zip")

if uploaded_zip:
    objetivo = st.text_input("Nombre de la función objetivo para todas las filas:", value="MIN COSTOS")
    nombre_archivo = st.text_input("Nombre del archivo CSV de salida:", value="Multimoora_PREP.csv")

    if objetivo and nombre_archivo:
        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            st.success(f"Se extrajeron {len(file_list)} archivos del ZIP.")

            dfs = []
            for file_name in file_list:
                if file_name.endswith('.xlsx'):
                    try:
                        with zip_ref.open(file_name) as file:
                            xls = pd.ExcelFile(file)
                            data = {}
                            for sheet in xls.sheet_names:
                                df_temp = pd.read_excel(xls, sheet_name=sheet)
                                if 'level' in df_temp.columns:
                                    valor = df_temp.loc[0, 'level']
                                    data[sheet.lower()] = valor

                            fila = {
                                'Lambda': data.get('lambda', None),
                                'Z': data.get('z', None),
                                'ENT': data.get('ent', None),
                                'VAR': data.get('varianza', None)
                            }
                            dfs.append(fila)
                    except Exception as e:
                        st.warning(f"⚠️ No se pudo procesar {file_name}: {str(e)}")

            if dfs:
                df_final = pd.DataFrame(dfs)

                # Conversión numérica explícita para mantener punto decimal
                for col in ['Lambda', 'Z', 'ENT', 'VAR']:
                    df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
                    df_final[col] = df_final[col].astype(float)

                df_final = df_final.sort_values(by='Lambda').reset_index(drop=True)
                df_final['Objetivo'] = objetivo
                df_final = df_final[['Lambda', 'Z', 'ENT', 'VAR', 'Objetivo']]  # orden correcto

                st.subheader("🧾 Resultado listo para MULTIMOORA:")
                st.dataframe(df_final)

                st.download_button(
                    label="📥 Descargar CSV transformado para MULTIMOORA",
                    data=df_final.to_csv(index=False, header=True, sep=';').encode('utf-8'),
                    file_name=nombre_archivo,
                    mime='text/csv'
                )
            else:
                st.error("❌ No se encontraron datos válidos en los archivos .xlsx del ZIP.")
