"""
Reporte ejecutivo en PDF de una corrida de auditoria.

Reutiliza los mismos DataFrames (df_facturas, df_hallazgos) que ya usan
main.py, menu.py y app.py -- no recalcula nada, solo los presenta en un
formato mas formal para enviar por correo o mostrar en la pasantia.
"""
from datetime import datetime

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)

from analisis import top_facturas_reincidentes, top_codigos_cups_reincidentes

MAX_FILAS_DETALLE = 60  # limite razonable para que el PDF no se vuelva enorme


def generar_pdf_resumen(df_facturas: pd.DataFrame, df_hallazgos: pd.DataFrame,
                         ruta_salida: str, tolerancia_totales: float = 0,
                         tolerancia_tarifario: float = 0):
    styles = getSampleStyleSheet()
    estilo_celda = ParagraphStyle(
        "celda", parent=styles["Normal"], fontSize=8, leading=10,
    )

    doc = SimpleDocTemplate(
        ruta_salida, pagesize=letter,
        leftMargin=48, rightMargin=48, topMargin=48, bottomMargin=48,
    )
    story = []

    story.append(Paragraph("SaludAudita - Reporte de auditoria", styles["Title"]))
    fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M")
    story.append(Paragraph(f"Generado: {fecha_generacion}", styles["Normal"]))
    story.append(Paragraph(
        f"Tolerancia usada — totales: ${tolerancia_totales:,.0f} | "
        f"tarifario: ${tolerancia_tarifario:,.0f}",
        styles["Normal"],
    ))
    story.append(Spacer(1, 16))

    # ---- Metricas principales ----
    story.append(Paragraph("Resumen", styles["Heading2"]))
    reglas_con_hallazgos = df_hallazgos["Regla"].nunique() if not df_hallazgos.empty else 0
    metricas = [
        ["Facturas analizadas", str(len(df_facturas))],
        ["Hallazgos encontrados", str(len(df_hallazgos))],
        ["Reglas con hallazgos", str(reglas_con_hallazgos)],
    ]
    tabla_metricas = Table(metricas, colWidths=[220, 100])
    tabla_metricas.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
    ]))
    story.append(tabla_metricas)
    story.append(Spacer(1, 16))

    # ---- Hallazgos por regla ----
    story.append(Paragraph("Hallazgos por regla", styles["Heading2"]))
    if df_hallazgos.empty:
        story.append(Paragraph("No se encontraron hallazgos.", styles["Normal"]))
    else:
        conteo_regla = df_hallazgos["Regla"].value_counts().reset_index()
        conteo_regla.columns = ["Regla", "Cantidad"]
        data_regla = [["Regla", "Cantidad"]] + conteo_regla.values.tolist()
        tabla_regla = Table(data_regla, colWidths=[320, 100])
        tabla_regla.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))
        story.append(tabla_regla)
    story.append(Spacer(1, 16))

    # ---- Reincidencias ----
    story.append(Paragraph("Facturas con mas hallazgos", styles["Heading2"]))
    top_facturas = top_facturas_reincidentes(df_hallazgos)
    if top_facturas.empty:
        story.append(Paragraph("Ninguna factura tiene 2 o mas hallazgos.", styles["Normal"]))
    else:
        data_top_fact = [list(top_facturas.columns)] + top_facturas.values.tolist()
        tabla_top_fact = Table(data_top_fact, colWidths=[150, 130, 130])
        tabla_top_fact.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))
        story.append(tabla_top_fact)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Codigos CUPS mas repetidos", styles["Heading2"]))
    top_cups = top_codigos_cups_reincidentes(df_hallazgos)
    if top_cups.empty:
        story.append(Paragraph("Ningun codigo CUPS se repite en 2 o mas facturas.", styles["Normal"]))
    else:
        data_top_cups = [list(top_cups.columns)] + top_cups.values.tolist()
        tabla_top_cups = Table(data_top_cups, colWidths=[150, 130, 130])
        tabla_top_cups.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))
        story.append(tabla_top_cups)

    story.append(PageBreak())

    # ---- Detalle de hallazgos ----
    story.append(Paragraph("Detalle de hallazgos", styles["Heading2"]))
    if df_hallazgos.empty:
        story.append(Paragraph("No se encontraron hallazgos.", styles["Normal"]))
    else:
        detalle = df_hallazgos[["N_Factura", "Regla", "Motivo_Hallazgo"]].head(MAX_FILAS_DETALLE)
        if len(df_hallazgos) > MAX_FILAS_DETALLE:
            story.append(Paragraph(
                f"Mostrando los primeros {MAX_FILAS_DETALLE} de {len(df_hallazgos)} "
                "hallazgos. El detalle completo esta en el reporte .xlsx/.csv.",
                styles["Normal"],
            ))
            story.append(Spacer(1, 8))

        data_detalle = [["N_Factura", "Regla", "Motivo"]]
        for _, fila in detalle.iterrows():
            data_detalle.append([
                Paragraph(str(fila["N_Factura"]), estilo_celda),
                Paragraph(str(fila["Regla"]), estilo_celda),
                Paragraph(str(fila["Motivo_Hallazgo"]), estilo_celda),
            ])

        tabla_detalle = Table(data_detalle, colWidths=[70, 140, 306], repeatRows=1)
        tabla_detalle.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(tabla_detalle)

    doc.build(story)
