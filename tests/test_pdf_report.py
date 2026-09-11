import os

import pandas as pd
import pdfplumber

from pdf_report import generar_pdf_resumen


def _dataset_pequeno():
    df_facturas = pd.DataFrame({
        "N_Factura": ["F1", "F2", "F3"],
        "Codigo_CUPS": ["890201", "890201", "620102"],
    })
    df_hallazgos = pd.DataFrame({
        "N_Factura": ["F1", "F1", "F2"],
        "Codigo_CUPS": ["890201", "890201", "890201"],
        "Regla": ["Soporte_Autorizacion", "Glosa_Mal_Aplicada", "Codigo_Invalido"],
        "Motivo_Hallazgo": ["Sin soporte", "Glosa repetida", "Codigo invalido"],
    })
    return df_facturas, df_hallazgos


def test_pdf_se_genera_y_contiene_las_metricas_correctas(tmp_path):
    df_facturas, df_hallazgos = _dataset_pequeno()
    ruta_pdf = str(tmp_path / "reporte.pdf")

    generar_pdf_resumen(df_facturas, df_hallazgos, ruta_pdf)

    assert os.path.exists(ruta_pdf)

    with pdfplumber.open(ruta_pdf) as pdf:
        texto_completo = "\n".join(p.extract_text() or "" for p in pdf.pages)

    assert "Facturas analizadas 3" in texto_completo
    assert "Hallazgos encontrados 3" in texto_completo
    assert "F1" in texto_completo
    assert "Sin soporte" in texto_completo


def test_pdf_muestra_reincidencia_de_f1(tmp_path):
    df_facturas, df_hallazgos = _dataset_pequeno()
    ruta_pdf = str(tmp_path / "reporte.pdf")

    generar_pdf_resumen(df_facturas, df_hallazgos, ruta_pdf)

    with pdfplumber.open(ruta_pdf) as pdf:
        texto_completo = "\n".join(p.extract_text() or "" for p in pdf.pages)

    # F1 tiene 2 hallazgos (Soporte_Autorizacion y Glosa_Mal_Aplicada) -> reincidente
    assert "Facturas con mas hallazgos" in texto_completo
    assert "F1" in texto_completo


def test_pdf_con_dataset_vacio_no_falla(tmp_path):
    df_facturas = pd.DataFrame({"N_Factura": [], "Codigo_CUPS": []})
    df_hallazgos = pd.DataFrame({"N_Factura": [], "Regla": [], "Motivo_Hallazgo": []})
    ruta_pdf = str(tmp_path / "reporte_vacio.pdf")

    generar_pdf_resumen(df_facturas, df_hallazgos, ruta_pdf)

    assert os.path.exists(ruta_pdf)
    with pdfplumber.open(ruta_pdf) as pdf:
        texto_completo = "\n".join(p.extract_text() or "" for p in pdf.pages)
    assert "No se encontraron hallazgos" in texto_completo


def test_pdf_muestra_tolerancias_usadas(tmp_path):
    df_facturas, df_hallazgos = _dataset_pequeno()
    ruta_pdf = str(tmp_path / "reporte_tol.pdf")

    generar_pdf_resumen(
        df_facturas, df_hallazgos, ruta_pdf,
        tolerancia_totales=5000, tolerancia_tarifario=2000,
    )

    with pdfplumber.open(ruta_pdf) as pdf:
        texto_completo = "\n".join(p.extract_text() or "" for p in pdf.pages)

    assert "5,000" in texto_completo
    assert "2,000" in texto_completo
