"""
Modulo de carga de datos para SaludAudita.
Lee el Excel simulado y devuelve DataFrames de pandas listos para validar.
"""
import pandas as pd


def cargar_facturas(ruta_excel: str) -> pd.DataFrame:
    """Carga la hoja 'Facturas' del Excel simulado."""
    # dtype=str en Codigo_CUPS evita que pandas interprete el codigo como numero
    # y pierda ceros a la izquierda (ej. "000000" -> 0). Bug detectado en fase 3.
    df = pd.read_excel(
        ruta_excel,
        sheet_name="Facturas",
        dtype={"Codigo_CUPS": str, "Diagnostico_CIE10": str},
    )
    # Normalizar tipos de texto para evitar falsos positivos por espacios/mayusculas
    for col in ["Tiene_Soporte", "Tiene_Autorizacion", "Codigo_CUPS", "Manual_Tarifario"]:
        df[col] = df[col].astype(str).str.strip()
    df["Glosa_Aplicada"] = df["Glosa_Aplicada"].fillna("").astype(str).str.strip()

    # Fechas: convertir a datetime para poder calcular dias habiles (regla 5)
    for col in ["Fecha_Servicio", "Fecha_Expedicion_Factura", "Fecha_Radicacion_Soportes"]:
        df[col] = pd.to_datetime(df[col])

    return df


def cargar_cups_validos(ruta_excel: str) -> pd.DataFrame:
    """Carga la hoja 'CUPS_Validos' del Excel simulado (tabla de referencia)."""
    df = pd.read_excel(ruta_excel, sheet_name="CUPS_Validos", dtype={"Codigo_CUPS": str})
    df["Codigo_CUPS"] = df["Codigo_CUPS"].astype(str).str.strip()
    return df
