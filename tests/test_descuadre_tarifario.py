import pandas as pd
from validators.descuadre_tarifario import validar_descuadre_tarifario


def _df(valor_unitario, valor_tarifario_ref, manual="SOAT"):
    return pd.DataFrame({
        "N_Factura": ["F1"],
        "Manual_Tarifario": [manual],
        "Valor_Unitario": [valor_unitario],
        "Valor_Tarifario_Referencia": [valor_tarifario_ref],
    })


def test_detecta_descuadre_tarifario():
    df = _df(40000, 85000)
    resultado = validar_descuadre_tarifario(df)
    assert len(resultado) == 1
    assert "Descuadre contra tarifario" in resultado.iloc[0]["Motivo_Hallazgo"]


def test_no_detecta_cuando_coincide():
    df = _df(40000, 40000)
    resultado = validar_descuadre_tarifario(df)
    assert len(resultado) == 0


def test_detecta_diferencia_negativa():
    df = _df(150000, 125000)
    resultado = validar_descuadre_tarifario(df)
    assert len(resultado) == 1


def test_tolerancia_personalizada():
    df = _df(40000, 40500)
    assert len(validar_descuadre_tarifario(df, tolerancia=0)) == 1
    assert len(validar_descuadre_tarifario(df, tolerancia=1000)) == 0


def test_tolerancia_se_puede_pasar_como_parametro_nombrado():
    df = _df(40000, 40500)
    assert len(validar_descuadre_tarifario(df, tolerancia=1000)) == 0
    assert len(validar_descuadre_tarifario(df, tolerancia=100)) == 1
