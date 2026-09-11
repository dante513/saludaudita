"""
SaludAudita - Orquestador principal.
Corre las 4 validaciones sobre el Excel simulado, persiste en SQLite
y exporta el reporte de hallazgos en Excel y CSV.

Puede usarse directamente (python main.py) o importarse desde menu.py
para el menu interactivo.
"""
import os

from loaders import cargar_facturas, cargar_cups_validos
from validators.soporte_autorizacion import validar_soporte_autorizacion
from validators.codigos_invalidos import validar_codigos_invalidos
from validators.glosas import validar_glosas
from validators.totales import validar_totales
from validators.devolucion_radicacion import validar_radicacion_extemporanea
from validators.descuadre_tarifario import validar_descuadre_tarifario
from report import consolidar_hallazgos, exportar_reporte
from db import (
    crear_conexion, guardar_facturas, guardar_cups_validos, guardar_hallazgos,
    guardar_historial_auditoria,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_EXCEL = os.path.join(BASE_DIR, "..", "data", "facturas_simuladas.xlsx")
RUTA_DB = os.path.join(BASE_DIR, "..", "saludaudita.db")
RUTA_SALIDA_XLSX = os.path.join(BASE_DIR, "..", "output", "reporte_hallazgos.xlsx")
RUTA_SALIDA_CSV = os.path.join(BASE_DIR, "..", "output", "reporte_hallazgos.csv")


def ejecutar_auditoria(tolerancia_totales: float = 0, tolerancia_tarifario: float = 0):
    """
    Corre el pipeline completo y devuelve (df_facturas, df_hallazgos).
    Esta funcion es el punto de entrada que usa tanto el modo consola simple
    como el menu interactivo. Ademas de guardar el resultado mas reciente,
    agrega la corrida al historial de auditorias en SQLite.
    """
    df_facturas = cargar_facturas(RUTA_EXCEL)
    df_cups = cargar_cups_validos(RUTA_EXCEL)

    hallazgos = [
        validar_soporte_autorizacion(df_facturas),
        validar_codigos_invalidos(df_facturas, df_cups),
        validar_glosas(df_facturas),
        validar_totales(df_facturas, tolerancia=tolerancia_totales),
        validar_radicacion_extemporanea(df_facturas),
        validar_descuadre_tarifario(df_facturas, tolerancia=tolerancia_tarifario),
    ]
    df_hallazgos = consolidar_hallazgos(hallazgos)

    # Persistencia en SQLite (fase 2, seccion 5)
    conn = crear_conexion(RUTA_DB)
    guardar_facturas(df_facturas, conn)
    guardar_cups_validos(df_cups, conn)
    guardar_hallazgos(df_hallazgos, conn)
    guardar_historial_auditoria(df_hallazgos, conn, tolerancia_totales, tolerancia_tarifario)
    conn.close()

    # Reporte final
    os.makedirs(os.path.join(BASE_DIR, "..", "output"), exist_ok=True)
    exportar_reporte(df_hallazgos, RUTA_SALIDA_XLSX, RUTA_SALIDA_CSV)

    return df_facturas, df_hallazgos


def main():
    df_facturas, df_hallazgos = ejecutar_auditoria()
    print(f"Total de facturas analizadas: {len(df_facturas)}")
    print(f"Total de hallazgos encontrados: {len(df_hallazgos)}")
    print("\nHallazgos por regla:")
    print(df_hallazgos["Regla"].value_counts().to_string())


if __name__ == "__main__":
    main()

