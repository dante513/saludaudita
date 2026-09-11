import sqlite3

import pandas as pd
from db import guardar_historial_auditoria, obtener_resumen_historial


def test_historial_se_acumula_entre_corridas():
    conn = sqlite3.connect(":memory:")

    df_corrida_1 = pd.DataFrame({
        "N_Factura": ["F1"],
        "Regla": ["Soporte_Autorizacion"],
    })
    df_corrida_2 = pd.DataFrame({
        "N_Factura": ["F2", "F3"],
        "Regla": ["Codigo_Invalido", "Codigo_Invalido"],
    })

    guardar_historial_auditoria(df_corrida_1, conn)
    guardar_historial_auditoria(df_corrida_2, conn)

    total = pd.read_sql("SELECT * FROM historial_auditorias", conn)
    conn.close()

    # Las 2 corridas deben coexistir (append), no solo la ultima (replace)
    assert len(total) == 3
    assert "Fecha_Auditoria" in total.columns


def test_resumen_historial_agrupa_por_fecha_y_regla():
    conn = sqlite3.connect(":memory:")
    df = pd.DataFrame({
        "N_Factura": ["F1", "F2", "F3"],
        "Regla": ["Codigo_Invalido", "Codigo_Invalido", "Descuadre_Totales"],
    })
    guardar_historial_auditoria(df, conn)

    resumen = obtener_resumen_historial(conn)
    conn.close()

    fila_cups = resumen[resumen["Regla"] == "Codigo_Invalido"].iloc[0]
    assert fila_cups["Cantidad"] == 2
