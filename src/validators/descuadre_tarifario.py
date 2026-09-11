"""
Regla 6: descuadre entre el valor facturado y el valor de referencia del
tarifario pactado (SOAT / ISS2001 / Particular).

Nota de transparencia: Valor_Tarifario_Referencia en el dataset simulado NO
proviene de un tarifario oficial real -- es un valor simulado para poder
probar esta regla. En un caso real, esta columna se llenaria cruzando contra
el tarifario/contrato vigente con cada EPS.
"""
import pandas as pd


def validar_descuadre_tarifario(df_facturas: pd.DataFrame, tolerancia: float = 0) -> pd.DataFrame:
    df = df_facturas.copy()
    df["_diferencia_tarifario"] = df["Valor_Unitario"] - df["Valor_Tarifario_Referencia"]

    mask = df["_diferencia_tarifario"].abs() > tolerancia
    hallazgos = df[mask].copy()
    hallazgos["Motivo_Hallazgo"] = (
        "Descuadre contra tarifario (" + hallazgos["Manual_Tarifario"] + "): "
        + "facturado " + hallazgos["Valor_Unitario"].astype(str)
        + " vs referencia " + hallazgos["Valor_Tarifario_Referencia"].astype(str)
    )
    hallazgos["Regla"] = "Descuadre_Tarifario"
    hallazgos = hallazgos.drop(columns=["_diferencia_tarifario"])
    return hallazgos
