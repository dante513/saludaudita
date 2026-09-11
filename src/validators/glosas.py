"""
Regla 3: glosas repetidas en la misma factura, o aplicadas sin que exista
una condicion que las justifique (sin soporte / sin autorizacion).
"""
import pandas as pd


def validar_glosas(df_facturas: pd.DataFrame) -> pd.DataFrame:
    con_glosa = df_facturas[df_facturas["Glosa_Aplicada"] != ""].copy()

    # Caso A: misma glosa repetida en la misma factura
    conteo = (
        con_glosa.groupby(["N_Factura", "Glosa_Aplicada"])
        .size()
        .reset_index(name="conteo")
    )
    repetidas = conteo[conteo["conteo"] > 1]
    claves_repetidas = set(zip(repetidas["N_Factura"], repetidas["Glosa_Aplicada"]))

    # Caso B: glosa aplicada sin que exista soporte/autorizacion faltante que la justifique
    def _sin_justificacion(row):
        if row["Glosa_Aplicada"] == "":
            return False
        justificada = (row["Tiene_Soporte"] == "No") or (row["Tiene_Autorizacion"] == "No")
        return not justificada

    con_glosa["_repetida"] = con_glosa.apply(
        lambda r: (r["N_Factura"], r["Glosa_Aplicada"]) in claves_repetidas, axis=1
    )
    con_glosa["_sin_justificacion"] = con_glosa.apply(_sin_justificacion, axis=1)

    mask = con_glosa["_repetida"] | con_glosa["_sin_justificacion"]
    hallazgos = con_glosa[mask].copy()

    def _motivo(row):
        motivos = []
        if row["_repetida"]:
            motivos.append("Glosa repetida en la misma factura")
        if row["_sin_justificacion"]:
            motivos.append("Glosa sin condicion que la justifique")
        return " y ".join(motivos)

    hallazgos["Motivo_Hallazgo"] = hallazgos.apply(_motivo, axis=1)
    hallazgos["Regla"] = "Glosa_Mal_Aplicada"
    hallazgos = hallazgos.drop(columns=["_repetida", "_sin_justificacion"])
    return hallazgos
