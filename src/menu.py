"""
SaludAudita - Menu interactivo por consola.
Punto de entrada recomendado para uso manual: python menu.py
"""
import os

from main import ejecutar_auditoria, RUTA_DB
from db import crear_conexion, obtener_resumen_historial
from analisis import top_facturas_reincidentes, top_codigos_cups_reincidentes
from pdf_report import generar_pdf_resumen


def mostrar_menu():
    print("\n===== SaludAudita - Menu principal =====")
    print("1. Ejecutar auditoria completa")
    print("2. Ver resumen de hallazgos por regla")
    print("3. Ver detalle de hallazgos de una regla")
    print("4. Buscar hallazgos de una factura especifica")
    print("5. Ver historial de auditorias anteriores")
    print("6. Ver reincidencias (facturas y codigos CUPS mas repetidos)")
    print("7. Exportar reporte ejecutivo en PDF")
    print("8. Salir")


def pedir_opcion():
    return input("Elige una opcion (1-8): ").strip()


def main():
    df_hallazgos = None
    df_facturas = None

    print("Bienvenido a SaludAudita - auditor de facturacion en salud")

    while True:
        mostrar_menu()
        opcion = pedir_opcion()

        if opcion == "1":
            df_facturas, df_hallazgos = ejecutar_auditoria()
            print(f"\nAuditoria completada: {len(df_facturas)} facturas analizadas, "
                  f"{len(df_hallazgos)} hallazgos encontrados.")
            print("Reporte guardado en output/reporte_hallazgos.xlsx y output/reporte_hallazgos.csv")

        elif opcion == "2":
            if df_hallazgos is None:
                print("\nPrimero debes ejecutar la auditoria (opcion 1).")
                continue
            print("\nHallazgos por regla:")
            print(df_hallazgos["Regla"].value_counts().to_string())

        elif opcion == "3":
            if df_hallazgos is None:
                print("\nPrimero debes ejecutar la auditoria (opcion 1).")
                continue
            reglas = sorted(df_hallazgos["Regla"].unique())
            print("\nReglas disponibles:")
            for i, r in enumerate(reglas, start=1):
                print(f"  {i}. {r}")
            seleccion = input("Elige el numero de la regla: ").strip()
            try:
                regla = reglas[int(seleccion) - 1]
            except (ValueError, IndexError):
                print("\nOpcion invalida.")
                continue
            subset = df_hallazgos[df_hallazgos["Regla"] == regla]
            print(f"\nHallazgos de la regla '{regla}' ({len(subset)}):")
            print(subset[["N_Factura", "Codigo_CUPS", "Motivo_Hallazgo"]].to_string(index=False))

        elif opcion == "4":
            if df_hallazgos is None:
                print("\nPrimero debes ejecutar la auditoria (opcion 1).")
                continue
            n_factura = input("Numero de factura (ej. FAC-1005): ").strip()
            subset = df_hallazgos[df_hallazgos["N_Factura"] == n_factura]
            if subset.empty:
                print(f"\nNo se encontraron hallazgos para la factura {n_factura}.")
            else:
                print(f"\nHallazgos de {n_factura}:")
                print(subset[["Regla", "Motivo_Hallazgo"]].to_string(index=False))

        elif opcion == "5":
            conn = crear_conexion(RUTA_DB)
            try:
                df_historial = obtener_resumen_historial(conn)
            finally:
                conn.close()
            if df_historial.empty:
                print("\nAun no hay corridas anteriores registradas.")
            else:
                print("\nHistorial de auditorias (por fecha y regla):")
                print(df_historial.to_string(index=False))

        elif opcion == "6":
            if df_hallazgos is None:
                print("\nPrimero debes ejecutar la auditoria (opcion 1).")
                continue
            top_facturas = top_facturas_reincidentes(df_hallazgos)
            top_cups = top_codigos_cups_reincidentes(df_hallazgos)
            print("\nFacturas con mas hallazgos (2 o mas):")
            if top_facturas.empty:
                print("  Ninguna factura tiene 2 o mas hallazgos.")
            else:
                print(top_facturas.to_string(index=False))
            print("\nCodigos CUPS mas repetidos entre hallazgos (2 o mas facturas):")
            if top_cups.empty:
                print("  Ningun codigo CUPS se repite en 2 o mas facturas.")
            else:
                print(top_cups.to_string(index=False))

        elif opcion == "7":
            if df_hallazgos is None:
                print("\nPrimero debes ejecutar la auditoria (opcion 1).")
                continue
            ruta_pdf = os.path.join(os.path.dirname(__file__), "..", "output", "reporte_resumen.pdf")
            generar_pdf_resumen(df_facturas, df_hallazgos, ruta_pdf)
            print(f"\nReporte ejecutivo en PDF guardado en: {ruta_pdf}")

        elif opcion == "8":
            print("\nHasta luego.")
            break

        else:
            print("\nOpcion invalida, intenta de nuevo.")


if __name__ == "__main__":
    main()
