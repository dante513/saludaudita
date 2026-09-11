import pandas as pd
from validators.codigos_invalidos import validar_codigos_invalidos


def test_detecta_codigo_no_registrado():
    facturas = pd.DataFrame({"N_Factura": ["F1"], "Codigo_CUPS": ["999999"]})
    cups_validos = pd.DataFrame({"Codigo_CUPS": ["890201"]})
    resultado = validar_codigos_invalidos(facturas, cups_validos)
    assert len(resultado) == 1


def test_no_detecta_codigo_valido():
    facturas = pd.DataFrame({"N_Factura": ["F1"], "Codigo_CUPS": ["890201"]})
    cups_validos = pd.DataFrame({"Codigo_CUPS": ["890201"]})
    resultado = validar_codigos_invalidos(facturas, cups_validos)
    assert len(resultado) == 0


def test_conserva_ceros_a_la_izquierda():
    # Caso borde detectado en fase 3: un codigo "000000" no debe convertirse en "0"
    facturas = pd.DataFrame({"N_Factura": ["F1"], "Codigo_CUPS": ["000000"]})
    cups_validos = pd.DataFrame({"Codigo_CUPS": ["890201"]})
    resultado = validar_codigos_invalidos(facturas, cups_validos)
    assert resultado.iloc[0]["Codigo_CUPS"] == "000000"
    assert "000000" in resultado.iloc[0]["Motivo_Hallazgo"]


def test_lista_validos_vacia_marca_todo_invalido():
    facturas = pd.DataFrame({"N_Factura": ["F1"], "Codigo_CUPS": ["890201"]})
    cups_validos = pd.DataFrame({"Codigo_CUPS": []})
    resultado = validar_codigos_invalidos(facturas, cups_validos)
    assert len(resultado) == 1
