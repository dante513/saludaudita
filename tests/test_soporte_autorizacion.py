import pandas as pd
from validators.soporte_autorizacion import validar_soporte_autorizacion


def _df(rows):
    return pd.DataFrame(rows, columns=["N_Factura", "Tiene_Soporte", "Tiene_Autorizacion"])


def test_detecta_sin_soporte():
    df = _df([["F1", "No", "Si"]])
    resultado = validar_soporte_autorizacion(df)
    assert len(resultado) == 1
    assert resultado.iloc[0]["Motivo_Hallazgo"] == "Sin soporte"


def test_detecta_sin_autorizacion():
    df = _df([["F1", "Si", "No"]])
    resultado = validar_soporte_autorizacion(df)
    assert len(resultado) == 1
    assert resultado.iloc[0]["Motivo_Hallazgo"] == "Sin autorizacion"


def test_detecta_ambos_motivos():
    df = _df([["F1", "No", "No"]])
    resultado = validar_soporte_autorizacion(df)
    assert resultado.iloc[0]["Motivo_Hallazgo"] == "Sin soporte y Sin autorizacion"


def test_no_detecta_caso_valido():
    df = _df([["F1", "Si", "Si"]])
    resultado = validar_soporte_autorizacion(df)
    assert len(resultado) == 0


def test_dataframe_vacio_no_falla():
    df = _df([])
    resultado = validar_soporte_autorizacion(df)
    assert len(resultado) == 0
