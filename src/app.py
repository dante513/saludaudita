"""
SaludAudita - Interfaz web (Streamlit).

Para correrlo:
    streamlit run app.py

Reutiliza los mismos modulos de src/ (loaders, validators, report) que usan
main.py y menu.py — la logica de auditoria es una sola, esto es solo una
interfaz distinta sobre ella.
"""
import io
import os

import streamlit as st

from loaders import cargar_facturas, cargar_cups_validos
from validators.soporte_autorizacion import validar_soporte_autorizacion
from validators.codigos_invalidos import validar_codigos_invalidos
from validators.glosas import validar_glosas
from validators.totales import validar_totales
from validators.devolucion_radicacion import validar_radicacion_extemporanea
from validators.descuadre_tarifario import validar_descuadre_tarifario
from report import consolidar_hallazgos
from analisis import top_facturas_reincidentes, top_codigos_cups_reincidentes
from pdf_report import generar_pdf_resumen
from db import (
    crear_conexion, guardar_facturas, guardar_cups_validos, guardar_hallazgos,
    guardar_historial_auditoria, obtener_resumen_historial,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_EXCEL_DEFAULT = os.path.join(BASE_DIR, "..", "data", "facturas_simuladas.xlsx")
RUTA_DB = os.path.join(BASE_DIR, "..", "saludaudita.db")

st.set_page_config(page_title="SaludAudita", layout="wide")

st.title("SaludAudita")
st.caption("Auditor automatico de facturacion en salud — proyecto de portafolio")

archivo_subido = st.file_uploader(
    "Sube un Excel de facturas (o deja vacio para usar el dataset simulado)",
    type=["xlsx"],
)

if archivo_subido is not None:
    fuente = archivo_subido
    st.info("Usando el archivo que subiste.")
else:
    fuente = RUTA_EXCEL_DEFAULT
    st.info("Usando el dataset simulado por defecto (data/facturas_simuladas.xlsx).")

st.subheader("Tolerancias de las reglas de descuadre")
st.caption(
    "Por defecto ambas son $0 (cualquier diferencia se marca). Súbelas si en la "
    "práctica se acepta un margen pequeño antes de considerarlo un hallazgo."
)
col_tol1, col_tol2 = st.columns(2)
tolerancia_totales = col_tol1.number_input(
    "Tolerancia — descuadre de totales ($)",
    min_value=0, value=0, step=1000,
    help="Diferencia máxima aceptada entre Valor_Unitario × Cantidad y el valor registrado.",
)
tolerancia_tarifario = col_tol2.number_input(
    "Tolerancia — descuadre tarifario ($)",
    min_value=0, value=0, step=1000,
    help="Diferencia máxima aceptada entre el valor facturado y el valor de referencia del tarifario.",
)

if st.button("Ejecutar auditoria", type="primary"):
    df_facturas = cargar_facturas(fuente)
    df_cups = cargar_cups_validos(fuente)

    hallazgos = [
        validar_soporte_autorizacion(df_facturas),
        validar_codigos_invalidos(df_facturas, df_cups),
        validar_glosas(df_facturas),
        validar_totales(df_facturas, tolerancia=tolerancia_totales),
        validar_radicacion_extemporanea(df_facturas),
        validar_descuadre_tarifario(df_facturas, tolerancia=tolerancia_tarifario),
    ]
    df_hallazgos = consolidar_hallazgos(hallazgos)

    conn = crear_conexion(RUTA_DB)
    guardar_facturas(df_facturas, conn)
    guardar_cups_validos(df_cups, conn)
    guardar_hallazgos(df_hallazgos, conn)
    guardar_historial_auditoria(df_hallazgos, conn, tolerancia_totales, tolerancia_tarifario)
    conn.close()

    st.session_state["df_facturas"] = df_facturas
    st.session_state["df_hallazgos"] = df_hallazgos
    st.session_state["tolerancias_usadas"] = (tolerancia_totales, tolerancia_tarifario)

if "df_hallazgos" in st.session_state:
    df_facturas = st.session_state["df_facturas"]
    df_hallazgos = st.session_state["df_hallazgos"]
    tol_tot_usada, tol_tar_usada = st.session_state["tolerancias_usadas"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Facturas analizadas", len(df_facturas))
    col2.metric("Hallazgos encontrados", len(df_hallazgos))
    col3.metric("Reglas con hallazgos", df_hallazgos["Regla"].nunique())
    st.caption(
        f"Calculado con tolerancia de totales = ${tol_tot_usada:,} y "
        f"tolerancia tarifaria = ${tol_tar_usada:,}."
    )

    st.subheader("Hallazgos por regla")
    st.bar_chart(df_hallazgos["Regla"].value_counts())

    st.subheader("Detalle de hallazgos")
    reglas_disponibles = ["Todas"] + sorted(df_hallazgos["Regla"].unique().tolist())
    col_a, col_b = st.columns(2)
    regla_filtro = col_a.selectbox("Filtrar por regla", reglas_disponibles)
    factura_filtro = col_b.text_input("Filtrar por N° de factura (ej. FAC-1005)")

    df_filtrado = df_hallazgos.copy()
    if regla_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Regla"] == regla_filtro]
    if factura_filtro:
        df_filtrado = df_filtrado[
            df_filtrado["N_Factura"].str.contains(factura_filtro, case=False, na=False)
        ]

    st.dataframe(df_filtrado, use_container_width=True)

    st.subheader("Reincidencias")
    st.caption("Facturas o códigos CUPS que aparecen repetidos entre los hallazgos — útil para priorizar la revisión manual.")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("**Facturas con más hallazgos**")
        top_facturas = top_facturas_reincidentes(df_hallazgos)
        if top_facturas.empty:
            st.write("Ninguna factura tiene 2 o más hallazgos.")
        else:
            st.dataframe(top_facturas, use_container_width=True)
    with col_r2:
        st.markdown("**Códigos CUPS más repetidos**")
        top_cups = top_codigos_cups_reincidentes(df_hallazgos)
        if top_cups.empty:
            st.write("Ningún código CUPS se repite en 2 o más facturas.")
        else:
            st.dataframe(top_cups, use_container_width=True)

    st.subheader("Descargar reporte")
    csv_bytes = df_hallazgos.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV", csv_bytes, "reporte_hallazgos.csv", "text/csv")

    buffer = io.BytesIO()
    df_hallazgos.to_excel(buffer, index=False)
    st.download_button(
        "Descargar Excel",
        buffer.getvalue(),
        "reporte_hallazgos.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    buffer_pdf = io.BytesIO()
    generar_pdf_resumen(
        df_facturas, df_hallazgos, buffer_pdf,
        tolerancia_totales=tol_tot_usada, tolerancia_tarifario=tol_tar_usada,
    )
    st.download_button(
        "Descargar reporte ejecutivo (PDF)",
        buffer_pdf.getvalue(),
        "reporte_ejecutivo.pdf",
        "application/pdf",
    )

    with st.expander("Historial de auditorías anteriores"):
        conn = crear_conexion(RUTA_DB)
        try:
            df_historial = obtener_resumen_historial(conn)
        finally:
            conn.close()
        if df_historial.empty:
            st.write("Aún no hay corridas anteriores registradas.")
        else:
            st.dataframe(df_historial, use_container_width=True)
else:
    st.write("Presiona **Ejecutar auditoria** para ver los resultados.")
