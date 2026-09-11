import pandas as pd
from analisis import top_facturas_reincidentes, top_codigos_cups_reincidentes


def _df(rows):
    return pd.DataFrame(rows, columns=["N_Factura", "Codigo_CUPS", "Regla"])


def test_detecta_factura_reincidente():
    df = _df([
        ["F1", "890201", "Soporte_Autorizacion"],
        ["F1", "890201", "Glosa_Mal_Aplicada"],
        ["F2", "620102", "Codigo_Invalido"],
    ])
    resultado = top_facturas_reincidentes(df)
    assert len(resultado) == 1
    assert resultado.iloc[0]["N_Factura"] == "F1"
    assert resultado.iloc[0]["Cantidad_Hallazgos"] == 2
    assert resultado.iloc[0]["Reglas_Distintas"] == 2


def test_no_hay_reincidencias_si_todas_son_unicas():
    df = _df([
        ["F1", "890201", "Soporte_Autorizacion"],
        ["F2", "620102", "Codigo_Invalido"],
    ])
    resultado = top_facturas_reincidentes(df)
    assert len(resultado) == 0


def test_ordena_de_mayor_a_menor_cantidad():
    df = _df([
        ["F1", "890201", "A"], ["F1", "890201", "B"],
        ["F2", "620102", "A"], ["F2", "620102", "B"], ["F2", "620102", "C"],
    ])
    resultado = top_facturas_reincidentes(df)
    assert resultado.iloc[0]["N_Factura"] == "F2"
    assert resultado.iloc[0]["Cantidad_Hallazgos"] == 3
    assert resultado.iloc[1]["N_Factura"] == "F1"


def test_top_n_limita_resultados():
    filas = []
    for i in range(5):
        filas.append([f"F{i}", "890201", "A"])
        filas.append([f"F{i}", "890201", "B"])
    df = _df(filas)
    resultado = top_facturas_reincidentes(df, top_n=2)
    assert len(resultado) == 2


def test_dataframe_vacio_no_falla():
    df = _df([])
    resultado = top_facturas_reincidentes(df)
    assert len(resultado) == 0


def test_detecta_codigo_cups_reincidente_en_facturas_distintas():
    df = _df([
        ["F1", "890201", "Codigo_Invalido"],
        ["F2", "890201", "Descuadre_Totales"],
        ["F3", "620102", "Glosa_Mal_Aplicada"],
    ])
    resultado = top_codigos_cups_reincidentes(df)
    assert len(resultado) == 1
    assert resultado.iloc[0]["Codigo_CUPS"] == "890201"
    assert resultado.iloc[0]["Cantidad_Hallazgos"] == 2
    assert resultado.iloc[0]["Facturas_Distintas"] == 2
