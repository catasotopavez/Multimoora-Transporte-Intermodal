
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
