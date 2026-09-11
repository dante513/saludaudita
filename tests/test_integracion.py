import os
import pandas as pd

from loaders import cargar_facturas, cargar_cups_validos
from validators.soporte_autorizacion import validar_soporte_autorizacion
from validators.codigos_invalidos import validar_codigos_invalidos
from validators.glosas import validar_glosas
from validators.totales import validar_totales
from validators.devolucion_radicacion import validar_radicacion_extemporanea
from validators.descuadre_tarifario import validar_descuadre_tarifario
from report import consolidar_hallazgos

RUTA_EXCEL = os.path.join(os.path.dirname(__file__), "..", "data", "facturas_simuladas.xlsx")


def test_pipeline_completo_sobre_dataset_simulado():
    df_facturas = cargar_facturas(RUTA_EXCEL)
    df_cups = cargar_cups_validos(RUTA_EXCEL)

    hallazgos = [
        validar_soporte_autorizacion(df_facturas),
        validar_codigos_invalidos(df_facturas, df_cups),
        validar_glosas(df_facturas),
        validar_totales(df_facturas),
        validar_radicacion_extemporanea(df_facturas),
        validar_descuadre_tarifario(df_facturas),
    ]
    df_hallazgos = consolidar_hallazgos(hallazgos)

    # No debe fallar y debe traer las columnas esperadas
    assert "Motivo_Hallazgo" in df_hallazgos.columns
    assert "Regla" in df_hallazgos.columns
    assert len(df_hallazgos) > 0
    assert df_hallazgos["Regla"].nunique() >= 4  # al menos varias reglas deben dispararse

    # El caso borde de ceros a la izquierda debe quedar corregido (fase 3 -> fase 4)
    invalidos = df_hallazgos[df_hallazgos["Regla"] == "Codigo_Invalido"]
    assert "0" not in invalidos["Codigo_CUPS"].values
