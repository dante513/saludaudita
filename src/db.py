"""
Modulo de persistencia en SQLite (segun lo definido en fase 2: Python + Pandas + SQL).
No se usa para las validaciones (eso lo hace pandas), sino para guardar
el dataset de referencia y los hallazgos como lo haria un sistema real.
"""
import sqlite3
from datetime import datetime

import pandas as pd


def crear_conexion(ruta_db: str) -> sqlite3.Connection:
    return sqlite3.connect(ruta_db)


def guardar_facturas(df_facturas: pd.DataFrame, conn: sqlite3.Connection):
    df_facturas.to_sql("facturas", conn, if_exists="replace", index=False)


def guardar_cups_validos(df_cups: pd.DataFrame, conn: sqlite3.Connection):
    df_cups.to_sql("cups_validos", conn, if_exists="replace", index=False)


def guardar_hallazgos(df_hallazgos: pd.DataFrame, conn: sqlite3.Connection):
    """Guarda el resultado de la corrida MAS RECIENTE (se sobreescribe)."""
    df_hallazgos.to_sql("hallazgos", conn, if_exists="replace", index=False)


def guardar_historial_auditoria(df_hallazgos: pd.DataFrame, conn: sqlite3.Connection,
                                 tolerancia_totales: float = 0, tolerancia_tarifario: float = 0):
    """
    Agrega (append, no sobreescribe) el resultado de esta corrida a la tabla
    historial_auditorias, con fecha/hora y las tolerancias usadas, para poder
    comparar auditorias de distintos momentos mas adelante.
    """
    df_historial = df_hallazgos.copy()
    df_historial["Fecha_Auditoria"] = datetime.now().isoformat(timespec="seconds")
    df_historial["Tolerancia_Totales_Usada"] = tolerancia_totales
    df_historial["Tolerancia_Tarifario_Usada"] = tolerancia_tarifario
    df_historial.to_sql("historial_auditorias", conn, if_exists="append", index=False)


def obtener_resumen_historial(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Devuelve un resumen por fecha de auditoria: cuantos hallazgos hubo y de
    que reglas, para poder comparar corridas pasadas.
    """
    query = """
        SELECT Fecha_Auditoria, Regla, COUNT(*) as Cantidad
        FROM historial_auditorias
        GROUP BY Fecha_Auditoria, Regla
        ORDER BY Fecha_Auditoria DESC
    """
    return pd.read_sql(query, conn)

