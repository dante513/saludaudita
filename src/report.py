"""
Consolida los hallazgos de todos los validadores y exporta el reporte final
en Excel y CSV (segun decision de fase 2).
"""
import pandas as pd


def consolidar_hallazgos(lista_dfs: list) -> pd.DataFrame:
    return pd.concat(lista_dfs, ignore_index=True, sort=False)


def exportar_reporte(df_hallazgos: pd.DataFrame, ruta_xlsx: str, ruta_csv: str):
    df_hallazgos.to_excel(ruta_xlsx, index=False)
    df_hallazgos.to_csv(ruta_csv, index=False)
