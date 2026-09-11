import pandas as pd
from validators.glosas import validar_glosas


def _df(rows):
    return pd.DataFrame(
        rows,
        columns=["N_Factura", "Tiene_Soporte", "Tiene_Autorizacion", "Glosa_Aplicada"],
    )


def test_detecta_glosa_repetida_misma_factura():
    df = _df([
        ["F1", "Si", "Si", "Falta soporte"],
        ["F1", "Si", "Si", "Falta soporte"],
    ])
    resultado = validar_glosas(df)
    assert len(resultado) == 2
    assert all("repetida" in m for m in resultado["Motivo_Hallazgo"])


def test_detecta_glosa_sin_justificacion():
    # Tiene glosa pero Tiene_Soporte y Tiene_Autorizacion son "Si" -> no hay motivo real
    df = _df([["F1", "Si", "Si", "Codigo no autorizado"]])
    resultado = validar_glosas(df)
    assert len(resultado) == 1
    assert "sin condicion que la justifique" in resultado.iloc[0]["Motivo_Hallazgo"]


def test_no_detecta_glosa_justificada_y_unica():
    df = _df([["F1", "No", "Si", "Falta soporte"]])
    resultado = validar_glosas(df)
    assert len(resultado) == 0


def test_sin_glosa_no_genera_hallazgo():
    df = _df([["F1", "Si", "Si", ""]])
    resultado = validar_glosas(df)
    assert len(resultado) == 0


def test_misma_glosa_en_facturas_distintas_no_es_repetida():
    df = _df([
        ["F1", "No", "Si", "Falta soporte"],
        ["F2", "No", "Si", "Falta soporte"],
    ])
    resultado = validar_glosas(df)
    assert len(resultado) == 0
