"""
Regla 5: devolucion por radicacion extemporanea de soportes.

Base normativa: Resolucion 2284 de 2023 (Manual Unico de Devoluciones, Glosas
y Respuestas, Ministerio de Salud y Proteccion Social), que establece como
causal taxativa de devolucion la no radicacion de los soportes dentro de los
22 dias habiles siguientes a la fecha de expedicion de la factura.

Limitacion declarada: el conteo de dias habiles aqui excluye solo sabados y
domingos (numpy.busday_count con el calendario por defecto), no excluye
festivos colombianos. Para un calculo 100% exacto habria que incorporar el
calendario de festivos.
"""
import numpy as np
import pandas as pd

DIAS_HABILES_LIMITE = 22


def validar_radicacion_extemporanea(df_facturas: pd.DataFrame) -> pd.DataFrame:
    df = df_facturas.copy()

    def _dias_habiles(row):
        inicio = row["Fecha_Expedicion_Factura"].date()
        fin = row["Fecha_Radicacion_Soportes"].date()
        return int(np.busday_count(inicio, fin))

    df["_dias_habiles_radicacion"] = df.apply(_dias_habiles, axis=1)
    mask = df["_dias_habiles_radicacion"] > DIAS_HABILES_LIMITE

    hallazgos = df[mask].copy()
    hallazgos["Motivo_Hallazgo"] = (
        "Devolucion por radicacion extemporanea: "
        + hallazgos["_dias_habiles_radicacion"].astype(str)
        + f" dias habiles (limite {DIAS_HABILES_LIMITE})"
    )
    hallazgos["Regla"] = "Devolucion_Radicacion_Extemporanea"
    hallazgos = hallazgos.drop(columns=["_dias_habiles_radicacion"])
    return hallazgos
