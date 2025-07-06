import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="4. Comparación de Soluciones", layout="wide")
st.title("📊 4. Comparación de Soluciones por Objetivo")

st.markdown("""
Esta página compara las soluciones obtenidas desde las distintas funciones objetivo aplicadas al modelo intermodal:

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

def buscar_hoja(hojas, clave):
    for nombre in hojas:
        if clave.lower() in nombre.lower().replace(" ", ""):
            return hojas[nombre]
    return pd.DataFrame()

def extraer_valor(df):
    return df["level"].iloc[0] if "level" in df.columns and not df.empty else None

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
        "Costos (z)": [], "Entropía (ent)": [], "Var costos (varianza)": [], "Demanda (perte)": [],
        "Nº terminales T": [], "Nº terminales S": [], "Rutas TS": [],
        "Cantidad de Terminales habilitados": [], "Tipos de modo utilizados": []
    }

    flujos_tipo = ["x_direct", "x_terminal_t", "x_terminal_s", "xt_tren", "xf_fluvial", "xc_carretera"]
    flujos_usados = {ft: [] for ft in flujos_tipo}

    for obj in objetivos:
        hojas = dfs[obj]
        z = extraer_valor(hojas.get("z", pd.DataFrame()))
        ent = extraer_valor(hojas.get("ent", pd.DataFrame()))
        var = extraer_valor(hojas.get("varianza", pd.DataFrame()))
        perte = extraer_valor(hojas.get("perte", pd.DataFrame()))

        indicadores["Costos (z)"].append(z)
        indicadores["Entropía (ent)"].append(ent)
        indicadores["Var costos (varianza)"].append(var)
        indicadores["Demanda (perte)"].append(perte)

        yt = buscar_hoja(hojas, "yt")
        ys = buscar_hoja(hojas, "ys")
        yst = buscar_hoja(hojas, "yst")

        n_yt = yt[yt.get("level", 0) > 0.5].shape[0] if not yt.empty else 0
        n_ys = ys[ys.get("level", 0) > 0.5].shape[0] if not ys.empty else 0
        n_yst = yst[yst["level"] > 0.5].shape[0] if not yst.empty and "level" in yst.columns else 0

        total_term = n_yt + n_ys

        indicadores["Nº terminales T"].append(n_yt)
        indicadores["Nº terminales S"].append(n_ys)
        indicadores["Rutas TS"].append(n_yst)
        indicadores["Cantidad de Terminales habilitados"].append(total_term)

        modos = []
        for tipo in flujos_tipo:
            hoja = hojas.get(tipo, pd.DataFrame())
            usados = hoja[hoja.get("level", 0) > 0].shape[0] if not hoja.empty else 0
            flujos_usados[tipo].append(usados)
            if usados > 0:
                modos.append(tipo)
        indicadores["Tipos de modo utilizados"].append(", ".join(modos))

    df_kpis = pd.DataFrame(indicadores, index=objetivos).T
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

    st.markdown("---")
    st.subheader("🔍 Ver detalle de una solución individual")

    opcion = st.selectbox("Selecciona una solución para explorar en detalle:", objetivos)

    if opcion:
        st.markdown(f"### 📌 Detalle para: **{opcion}**")
        hojas = dfs[opcion]

        z = extraer_valor(hojas.get("z", pd.DataFrame()))
        ent = extraer_valor(hojas.get("ent", pd.DataFrame()))
        var = extraer_valor(hojas.get("varianza", pd.DataFrame()))
        perte = extraer_valor(hojas.get("perte", pd.DataFrame()))

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Costo (Z)", round(z, 2) if pd.notnull(z) else "N/A")
        col2.metric("🔀 Entropía", round(ent, 2) if pd.notnull(ent) else "N/A")
        col3.metric("📉 Varianza", round(var, 2) if pd.notnull(var) else "N/A")
        col4.metric("📦 Demanda cubierta", round(perte, 2) if pd.notnull(perte) else "N/A")

        st.markdown("#### 🚛 Tablas de flujos utilizados por tipo")

        for tipo in flujos_tipo:
            hoja = hojas.get(tipo, pd.DataFrame())
            if not hoja.empty and "level" in hoja.columns:
                con_datos = hoja[hoja["level"] > 0]
                with st.expander(f"📦 {tipo} ({len(con_datos)} flujos utilizados)"):
                    st.dataframe(con_datos)

                    if tipo == "x_direct" and st.button("🔁 Mostrar grafo de x_direct"):
                        df = hoja[hoja["level"] > 0].rename(columns={"Unnamed: 0": "origen", "Unnamed: 1": "destino"})
                        G = nx.DiGraph()
                        G.add_edges_from(df[["origen", "destino"]].values)
                        pos = {n: (0, -i) for i, n in enumerate(df["origen"].unique())}
                        pos.update({n: (1, -i) for i, n in enumerate(df["destino"].unique())})
                        fig, ax = plt.subplots(figsize=(10, 6))
                        nx.draw(G, pos, with_labels=True, node_size=1200, node_color="lightblue", ax=ax)
                        st.pyplot(fig)

                    if tipo == "x_terminal_t" and st.button("🔁 Mostrar grafo de x_terminal_t"):
                        df = hoja[hoja["level"] > 0].rename(columns={"Unnamed: 0": "origen", "Unnamed: 1": "destino", "Unnamed: 2": "terminal"})
                        G = nx.DiGraph()
                        for _, row in df.iterrows():
                            G.add_edge(row["origen"], row["terminal"])
                            G.add_edge(row["terminal"], row["destino"])
                        pos = {}
                        origenes = df["origen"].unique()
                        terminales = df["terminal"].unique()
                        destinos = df["destino"].unique()
                        for i, n in enumerate(origenes):
                            pos[n] = (0, -i)
                        for i, n in enumerate(terminales):
                            pos[n] = (1, -i)
                        for i, n in enumerate(destinos):
                            pos[n] = (2, -i)
                        fig, ax = plt.subplots(figsize=(10, 6))
                        nx.draw(G, pos, with_labels=True, node_size=1200, node_color="lightblue", ax=ax)
                        st.pyplot(fig)
                    if tipo == "x_terminal_s" and st.button("🔁 Mostrar grafo de x_terminal_s"):
                        df = hoja[hoja["level"] > 0].rename(columns={"Unnamed: 0": "origen", "Unnamed: 1": "destino", "Unnamed: 2": "terminal"})
                        G = nx.DiGraph()
                        for _, row in df.iterrows():
                            G.add_edge(row["origen"], row["terminal"])
                            G.add_edge(row["terminal"], row["destino"])
                        pos = {}
                        origenes = df["origen"].unique()
                        terminales = df["terminal"].unique()
                        destinos = df["destino"].unique()
                        for i, n in enumerate(origenes):
                            pos[n] = (0, -i)
                        for i, n in enumerate(terminales):
                            pos[n] = (1, -i)
                        for i, n in enumerate(destinos):
                            pos[n] = (2, -i)
                        fig, ax = plt.subplots(figsize=(10, 6))
                        nx.draw(G, pos, with_labels=True, node_size=1200, node_color="lightblue", ax=ax)
                        st.pyplot(fig)
                    elif tipo in ["xt_tren", "xf_fluvial", "xc_carretera"] and st.button(f"🔁 Mostrar grafo de {tipo}"):
                        df = hoja[hoja["level"] > 0]
                        
                        # Asegúrate de que tenga al menos 5 columnas
                        if not df.empty and df.shape[1] >= 5:
                            # Renombra para facilitar
                            df = df.rename(columns={
                                df.columns[0]: "origen",
                                df.columns[1]: "destino",
                                df.columns[2]: "terminal_t",
                                df.columns[3]: "terminal_s"
                            })

                            G = nx.DiGraph()

                            for _, row in df.iterrows():
                                i, j, t, s = row["origen"], row["destino"], row["terminal_t"], row["terminal_s"]
                                G.add_edge(i, t)
                                G.add_edge(t, s)
                                G.add_edge(s, j)

                            # Extraer nodos únicos
                            nodos_i = df["origen"].unique().tolist()
                            nodos_t = df["terminal_t"].unique().tolist()
                            nodos_s = df["terminal_s"].unique().tolist()
                            nodos_j = df["destino"].unique().tolist()

                            pos = {}
                            for idx, n in enumerate(nodos_i):
                                pos[n] = (0, -idx)
                            for idx, n in enumerate(nodos_t):
                                pos[n] = (1, -idx)
                            for idx, n in enumerate(nodos_s):
                                pos[n] = (2, -idx)
                            for idx, n in enumerate(nodos_j):
                                pos[n] = (3, -idx)

                            fig, ax = plt.subplots(figsize=(12, 6))
                            nx.draw(G, pos, with_labels=True, node_size=1500, node_color="lightblue", arrows=True, ax=ax)
                            st.pyplot(fig)
                        else:
                            st.warning(f"❗ La hoja '{tipo}' no tiene datos suficientes para graficar.")

                    
                    
else:
    st.warning("📌 Sube los 4 archivos para ver la comparación.")
