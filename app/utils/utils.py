
import pandas as pd

def load_and_clean_csv(filepath, objetivo_label):
    df_raw = pd.read_csv(filepath, sep=';')  # ← ¡ESTO ES CLAVE!

    columnas_esperadas = ['Lambda', 'Z', 'ENT', 'VAR']
    for col in columnas_esperadas:
        if col not in df_raw.columns:
            raise ValueError(f"Falta la columna requerida: {col}")

    df_raw = df_raw[columnas_esperadas].copy()

    # Limpieza opcional
    for col in columnas_esperadas:
        df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

    df_raw = df_raw.dropna(subset=columnas_esperadas)
    df_raw['Objetivo'] = objetivo_label

    return df_raw[['Objetivo'] + columnas_esperadas]

def normalize_criteria(df):
    normalized = df.copy()

    for col in ['Z', 'VAR']:
        xmax = df[col].max()
        xmin = df[col].min()
        normalized[col] = (xmax - df[col]) / (xmax - xmin) if xmax != xmin else 1

    xmax = df['ENT'].max()
    xmin = df['ENT'].min()
    normalized['ENT'] = (df['ENT'] - xmin) / (xmax - xmin) if xmax != xmin else 1

    normalized['Lambda'] = df['Lambda']
    return normalized

def run_multimoora(df_combined, weights):
    df_normalized = normalize_criteria(df_combined)
    df_normalized['Objetivo'] = df_combined['Objetivo']

    df_weighted = df_normalized.copy()
    for col in ['Z', 'ENT', 'VAR', 'Lambda']:
        df_weighted[col] *= weights[col]

    df_weighted['Objetivo'] = df_combined['Objetivo']
    df_weighted['Lambda_val'] = df_combined['Lambda']

    df_weighted['RatioSystem'] = df_weighted[['Z', 'ENT', 'VAR', 'Lambda']].sum(axis=1)

    ideal = {col: df_weighted[col].max() for col in ['Z', 'ENT', 'VAR', 'Lambda']}
    df_weighted['ReferencePoint'] = df_weighted.apply(
        lambda row: max(abs(ideal[c] - row[c]) for c in ideal), axis=1
    )

    df_weighted['FMF'] = (
        (df_normalized['Z'] ** weights['Z']) *
        (df_normalized['ENT'] ** weights['ENT']) *
        (df_normalized['VAR'] ** weights['VAR']) *
        (df_normalized['Lambda'] ** weights['Lambda'])
    )

    df_weighted['Rank_RS'] = df_weighted['RatioSystem'].rank(ascending=False)
    df_weighted['Rank_RP'] = df_weighted['ReferencePoint'].rank(ascending=True)
    df_weighted['Rank_FMF'] = df_weighted['FMF'].rank(ascending=False)

    df_weighted['Ranking_Suma'] = (
        df_weighted['Rank_RS'] +
        df_weighted['Rank_RP'] +
        df_weighted['Rank_FMF']
    )
    df_weighted['Ranking_Final_Suma'] = df_weighted['Ranking_Suma'].rank(ascending=True)

    df_weighted['Ranking_Promedio'] = (
        df_weighted[['Rank_RS', 'Rank_RP', 'Rank_FMF']].mean(axis=1)
    )
    df_weighted['Ranking_Final_Promedio'] = df_weighted['Ranking_Promedio'].rank(ascending=True)

    return df_normalized, df_weighted
import networkx as nx
import matplotlib.pyplot as plt

def graficar_flujo_completo(hojas):
    G = nx.DiGraph()
    colores = {
        "x_direct": "blue",
        "x_terminal_t": "green",
        "x_terminal_s": "purple",
        "xt_tren": "orange",
        "xf_fluvial": "cyan",
        "xc_carretera": "red",
    }

    pos = {}
    layer_offset = {"I": 0, "T": 1, "S": 2, "J": 3}
    nodos_por_capa = {"I": set(), "T": set(), "S": set(), "J": set()}

    for tipo, color in colores.items():
        df = hojas.get(tipo, None)
        if df is None or "level" not in df.columns:
            continue
        activos = df[df["level"] > 0]

        if tipo == "x_direct":
            activos = activos.rename(columns={"Unnamed: 0": "i", "Unnamed: 1": "j"})
            for _, row in activos.iterrows():
                i, j = row["i"], row["j"]
                G.add_edge(i, j, color=color)
                nodos_por_capa["I"].add(i)
                nodos_por_capa["J"].add(j)

        elif tipo in ["x_terminal_t", "x_terminal_s"]:
            activos = activos.rename(columns={"Unnamed: 0": "i", "Unnamed: 1": "j", "Unnamed: 2": "t"})
            for _, row in activos.iterrows():
                i, j, t = row["i"], row["j"], row["t"]
                G.add_edge(i, t, color=color)
                G.add_edge(t, j, color=color)
                nodos_por_capa["I"].add(i)
                if tipo == "x_terminal_t":
                    nodos_por_capa["T"].add(t)
                else:
                    nodos_por_capa["S"].add(t)
                nodos_por_capa["J"].add(j)

        elif tipo in ["xt_tren", "xf_fluvial", "xc_carretera"]:
            activos = activos.rename(columns={
                activos.columns[0]: "i",
                activos.columns[1]: "j",
                activos.columns[2]: "t",
                activos.columns[3]: "s"
            })
            for _, row in activos.iterrows():
                i, j, t, s = row["i"], row["j"], row["t"], row["s"]
                G.add_edge(i, t, color=color)
                G.add_edge(t, s, color=color)
                G.add_edge(s, j, color=color)
                nodos_por_capa["I"].add(i)
                nodos_por_capa["T"].add(t)
                nodos_por_capa["S"].add(s)
                nodos_por_capa["J"].add(j)

    # Posiciones por capas
    for capa, nodos in nodos_por_capa.items():
        offset = layer_offset[capa]
        for idx, nodo in enumerate(sorted(nodos)):
            pos[nodo] = (offset, -idx)

    # Dibujar grafo
    fig, ax = plt.subplots(figsize=(14, 8))
    colores_aristas = [d["color"] for _, _, d in G.edges(data=True)]
    nx.draw(G, pos, with_labels=True, node_size=1500, edge_color=colores_aristas, arrows=True, ax=ax)
    return fig
