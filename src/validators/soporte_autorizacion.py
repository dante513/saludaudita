"""
Regla 1: servicios/procedimientos sin soporte o sin autorizacion.
"""
import pandas as pd


def validar_soporte_autorizacion(df_facturas: pd.DataFrame) -> pd.DataFrame:
    mask = (df_facturas["Tiene_Soporte"] == "No") | (df_facturas["Tiene_Autorizacion"] == "No")
    hallazgos = df_facturas[mask].copy()

    def _motivo(row):
        motivos = []
        if row["Tiene_Soporte"] == "No":
            motivos.append("Sin soporte")
        if row["Tiene_Autorizacion"] == "No":
            motivos.append("Sin autorizacion")
        return " y ".join(motivos)

    hallazgos["Motivo_Hallazgo"] = hallazgos.apply(_motivo, axis=1)
    hallazgos["Regla"] = "Soporte_Autorizacion"
    return hallazgos
