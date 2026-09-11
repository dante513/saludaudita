"""
Regla 4: descuadres en totales/valores facturados.
Valor_Unitario x Cantidad debe ser igual a Valor_Total_Registrado
(la columna Diferencia ya viene calculada por formula en el Excel).
"""
import pandas as pd


def validar_totales(df_facturas: pd.DataFrame, tolerancia: float = 0) -> pd.DataFrame:
    mask = df_facturas["Diferencia"].abs() > tolerancia
    hallazgos = df_facturas[mask].copy()
    hallazgos["Motivo_Hallazgo"] = (
        "Descuadre de totales: diferencia = " + hallazgos["Diferencia"].astype(str)
    )
    hallazgos["Regla"] = "Descuadre_Totales"
    return hallazgos
