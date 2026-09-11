import pandas as pd
from validators.devolucion_radicacion import validar_radicacion_extemporanea


def _df(fecha_expedicion, fecha_radicacion):
    return pd.DataFrame({
        "N_Factura": ["F1"],
        "Fecha_Expedicion_Factura": [pd.Timestamp(fecha_expedicion)],
        "Fecha_Radicacion_Soportes": [pd.Timestamp(fecha_radicacion)],
    })


def test_detecta_radicacion_fuera_de_22_dias_habiles():
    # Lunes 2026-01-05 a Lunes 2026-02-09: mas de 22 dias habiles
    df = _df("2026-01-05", "2026-02-09")
    resultado = validar_radicacion_extemporanea(df)
    assert len(resultado) == 1
    assert "Devolucion por radicacion extemporanea" in resultado.iloc[0]["Motivo_Hallazgo"]


def test_no_detecta_radicacion_dentro_del_plazo():
    # Solo unos pocos dias habiles de diferencia
    df = _df("2026-01-05", "2026-01-12")
    resultado = validar_radicacion_extemporanea(df)
    assert len(resultado) == 0


def test_exactamente_22_dias_habiles_no_se_marca():
    # 2026-01-05 -> 2026-02-04 = exactamente 22 dias habiles (verificado con
    # numpy.busday_count). La regla es > 22, no >=, asi que no debe marcarse.
    df = _df("2026-01-05", "2026-02-04")
    resultado = validar_radicacion_extemporanea(df)
    assert len(resultado) == 0


def test_23_dias_habiles_si_se_marca():
    # 2026-01-05 -> 2026-02-05 = exactamente 23 dias habiles (verificado con
    # numpy.busday_count): un dia habil por encima del limite, debe marcarse.
    df = _df("2026-01-05", "2026-02-05")
    resultado = validar_radicacion_extemporanea(df)
    assert len(resultado) == 1
