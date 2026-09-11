import pandas as pd
from validators.totales import validar_totales


def test_detecta_descuadre():
    df = pd.DataFrame({"N_Factura": ["F1"], "Diferencia": [10000]})
    resultado = validar_totales(df)
    assert len(resultado) == 1


def test_no_detecta_cuando_cuadra():
    df = pd.DataFrame({"N_Factura": ["F1"], "Diferencia": [0]})
    resultado = validar_totales(df)
    assert len(resultado) == 0


def test_detecta_diferencia_negativa():
    df = pd.DataFrame({"N_Factura": ["F1"], "Diferencia": [-5000]})
    resultado = validar_totales(df)
    assert len(resultado) == 1


def test_tolerancia_personalizada():
    df = pd.DataFrame({"N_Factura": ["F1"], "Diferencia": [50]})
    # con tolerancia 0 se detecta, con tolerancia 100 no
    assert len(validar_totales(df, tolerancia=0)) == 1
    assert len(validar_totales(df, tolerancia=100)) == 0


def test_tolerancia_se_puede_pasar_como_parametro_nombrado():
    # Verifica que la firma de la funcion realmente acepta 'tolerancia' con
    # nombre (necesario para que app.py se lo pueda pasar desde la interfaz).
    df = pd.DataFrame({"N_Factura": ["F1"], "Diferencia": [500]})
    assert len(validar_totales(df, tolerancia=1000)) == 0
    assert len(validar_totales(df, tolerancia=100)) == 1
