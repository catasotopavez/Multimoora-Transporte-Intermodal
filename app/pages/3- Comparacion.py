import streamlit as st
import pandas as pd

st.set_page_config(page_title="4. Comparación de Soluciones", layout="wide")
st.title("📊 4. Comparación de Soluciones por Objetivo")

st.markdown("Esta página compara las soluciones obtenidas desde las distintas funciones objetivo aplicadas al modelo intermodal:")

st.markdown("""
- ✅ Mínimo Costo  
- ✅ Máxima Entropía  
- ✅ Mínima Varianza  
- ✅ Máxima Demanda  
""")

st.markdown("---")
st.subheader("📁 Cargar archivos de resultados (uno por cada objetivo)")

col1, col2 = st.columns(2)
file_min_costos = col1.file_uploader("📥 Mínimo Costo", type=["xlsx"])
file_max_entropia = col2.file_uploader("📥 Máxima Entropía", type=["xlsx"])
file_min_var = col1.file_uploader("📥 Mínima Varianza", type=["xlsx"])
file_max_demanda = col2.file_uploader("📥 Máxima Demanda", type=["xlsx"])

# Función robusta para buscar hoja por nombre parcial e ignorar mayúsculas o espacios
def buscar_hoja(hojas, clave):
    for nombre in hojas:
        if clave.lower() in nombre.lower().replace(" ", ""):
            return hojas[nombre]
    return pd.DataFrame()

if all([file_min_costos, file_max_entropia, file_min_var, file_max_demanda]):
    dfs = {}
    files = {
        "Min Costos": file_min_costos,
        "Max Entropía": file_max_entropia,
        "Min Varianza": file_min_var,
        "Max Demanda": file_max_demanda,
    }

    for nombre, archivo in files.items():
        try:
            xls = pd.ExcelFile(archivo)
            sheets = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
            dfs[nombre] = sheets
            st.success(f"✅ {nombre} cargado correctamente con {len(sheets)} hojas")
        except Exception as e:
            st.error(f"❌ Error al leer {nombre}: {e}")

    st.markdown("---")
    st.subheader("📊 Comparación automática de indicadores y flujos")

    objetivos = list(dfs.keys())
    indicadores = {
        "Costos (z)": [],
        "Entropía (ent)": [],
        "Var costos (varianza)": [],
        "Demanda (perte)": [],
        "Nº terminales T": [],
        "Nº terminales S": [],
        "Rutas TS": [],
        "Cantidad de Terminales habilitados": [],
        "Tipos de modo utilizados": []
    }
    

    flujos_tipo = ["x_direct", "x_terminal_t", "x_terminal_s", "xt_tren", "xf_fluvial", "xc_carretera"]
    flujos_usados = {ft: [] for ft in flujos_tipo}
    print("cleaar")
    for obj in objetivos:
        hojas = dfs[obj]

        z = hojas.get("z", pd.DataFrame()).get("level", [None])[0]
        ent = hojas.get("ent", pd.DataFrame()).get("level", [None])[0]
        var = hojas.get("varianza", pd.DataFrame()).get("level", [None])[0]
        perte = hojas.get("perte", pd.DataFrame()).get("level", [None])[0]

        indicadores["Costos (z)"].append(z)
        indicadores["Entropía (ent)"].append(ent)
        indicadores["Var costos (varianza)"].append(var)
        indicadores["Demanda (perte)"].append(perte)

        yt = buscar_hoja(hojas, "yt")
        ys = buscar_hoja(hojas, "ys")
        yst = buscar_hoja(hojas, "yst")

        n_yt = yt[yt.get("level", 0) > 0.5].shape[0] if not yt.empty else 0
        n_ys = ys[ys.get("level", 0) > 0.5].shape[0] if not ys.empty else 0
        if not yst.empty and "level" in yst.columns:
            n_yst = yst[yst["level"] > 0.5].shape[0]
        else:
            n_yst = 0

        total_term = n_yt + n_ys

        indicadores["Nº terminales T"].append(n_yt)
        indicadores["Nº terminales S"].append(n_ys)
        indicadores["Rutas TS"].append(n_yst)
        indicadores["Cantidad de Terminales habilitados"].append(total_term)
        print(yst)

        modos = []
        for tipo in flujos_tipo:
            hoja = hojas.get(tipo, pd.DataFrame())
            usados = hoja[hoja.get("level", 0) > 0].shape[0] if not hoja.empty else 0
            flujos_usados[tipo].append(usados)
            if usados > 0:
                modos.append(tipo)
        indicadores["Tipos de modo utilizados"].append(", ".join(modos))

    df_kpis = pd.DataFrame(indicadores, index=objetivos).T
    #df_kpis = df_kpis.applymap(lambda x: x if isinstance(x, str) else round(x, 4) if pd.notnull(x) else x)
    df_kpis.loc["Tipos de modo utilizados"] = df_kpis.loc["Tipos de modo utilizados"].astype(str)
    for fila in df_kpis.index:
        if fila != "Tipos de modo utilizados":
            df_kpis.loc[fila] = pd.to_numeric(df_kpis.loc[fila], errors='coerce').round(4)

    st.subheader("📋 Tabla comparativa de indicadores")
    st.dataframe(df_kpis, use_container_width=True)

    df_flujos = pd.DataFrame(flujos_usados, index=objetivos).T
    df_flujos.index.name = "Tipo de flujo"
    st.subheader("🚚 Tabla comparativa de flujos utilizados")
    st.dataframe(df_flujos, use_container_width=True)
    
else:
    st.warning("📌 Sube los 4 archivos para ver la comparación.")
