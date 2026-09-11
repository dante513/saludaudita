"""
Regla 2: codigos CUPS/CIE10 invalidos o no autorizados
(no existen en la tabla de referencia CUPS_Validos).
"""
import pandas as pd


def validar_codigos_invalidos(df_facturas: pd.DataFrame, df_cups_validos: pd.DataFrame) -> pd.DataFrame:
    codigos_validos = set(df_cups_validos["Codigo_CUPS"])
    mask = ~df_facturas["Codigo_CUPS"].isin(codigos_validos)
    hallazgos = df_facturas[mask].copy()
    hallazgos["Motivo_Hallazgo"] = "Codigo CUPS invalido o no autorizado: " + hallazgos["Codigo_CUPS"]
    hallazgos["Regla"] = "Codigo_Invalido"
    return hallazgos
