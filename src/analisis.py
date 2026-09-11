"""
Analisis de reincidencias sobre los hallazgos ya generados.

No agrega reglas de negocio nuevas -- solo agrupa los hallazgos existentes
para responder: que facturas o que codigos CUPS se repiten mas seguido con
problemas, para priorizar donde enfocar la revision manual primero.
"""
import pandas as pd


def top_facturas_reincidentes(df_hallazgos: pd.DataFrame, minimo: int = 2, top_n: int = 10) -> pd.DataFrame:
    """
    Facturas que aparecen en 2 o mas hallazgos (posiblemente por reglas
    distintas). Ordenado por cantidad de hallazgos, de mayor a menor.
    """
    if df_hallazgos.empty:
        return pd.DataFrame(columns=["N_Factura", "Cantidad_Hallazgos", "Reglas_Distintas"])

    resumen = (
        df_hallazgos.groupby("N_Factura")
        .agg(Cantidad_Hallazgos=("Regla", "size"), Reglas_Distintas=("Regla", "nunique"))
        .reset_index()
    )
    resumen = resumen[resumen["Cantidad_Hallazgos"] >= minimo]
    resumen = resumen.sort_values(
        ["Cantidad_Hallazgos", "Reglas_Distintas"], ascending=False
    ).reset_index(drop=True)
    return resumen.head(top_n)


def top_codigos_cups_reincidentes(df_hallazgos: pd.DataFrame, minimo: int = 2, top_n: int = 10) -> pd.DataFrame:
    """
    Codigos CUPS que aparecen repetidos entre distintos hallazgos (en
    distintas facturas), para detectar patrones por tipo de servicio y no
    solo casos aislados.
    """
    if df_hallazgos.empty:
        return pd.DataFrame(columns=["Codigo_CUPS", "Cantidad_Hallazgos", "Facturas_Distintas"])

    resumen = (
        df_hallazgos.groupby("Codigo_CUPS")
        .agg(Cantidad_Hallazgos=("Regla", "size"), Facturas_Distintas=("N_Factura", "nunique"))
        .reset_index()
    )
    resumen = resumen[resumen["Cantidad_Hallazgos"] >= minimo]
    resumen = resumen.sort_values(
        ["Cantidad_Hallazgos", "Facturas_Distintas"], ascending=False
    ).reset_index(drop=True)
    return resumen.head(top_n)
