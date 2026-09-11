import os
import subprocess
import sys

SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "src")


def test_menu_corre_sin_errores_y_responde_opciones():
    entrada_usuario = "1\n2\n8\n"  # ejecutar auditoria, ver resumen, salir
    resultado = subprocess.run(
        [sys.executable, "menu.py"],
        cwd=SRC_DIR,
        input=entrada_usuario,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "Auditoria completada" in resultado.stdout
    assert "Hallazgos por regla" in resultado.stdout
    assert "Hasta luego" in resultado.stdout


def test_menu_opcion_invalida_no_lo_tumba():
    entrada_usuario = "9\n8\n"  # opcion invalida (9 no existe), luego salir
    resultado = subprocess.run(
        [sys.executable, "menu.py"],
        cwd=SRC_DIR,
        input=entrada_usuario,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "Opcion invalida" in resultado.stdout


def test_menu_muestra_historial_tras_ejecutar_auditoria():
    entrada_usuario = "1\n5\n8\n"  # ejecutar auditoria, ver historial, salir
    resultado = subprocess.run(
        [sys.executable, "menu.py"],
        cwd=SRC_DIR,
        input=entrada_usuario,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "Historial de auditorias" in resultado.stdout


def test_menu_muestra_reincidencias_tras_ejecutar_auditoria():
    entrada_usuario = "1\n6\n8\n"  # ejecutar auditoria, ver reincidencias, salir
    resultado = subprocess.run(
        [sys.executable, "menu.py"],
        cwd=SRC_DIR,
        input=entrada_usuario,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "Facturas con mas hallazgos" in resultado.stdout
    assert "Codigos CUPS mas repetidos" in resultado.stdout


def test_menu_exporta_pdf_tras_ejecutar_auditoria():
    entrada_usuario = "1\n7\n8\n"  # ejecutar auditoria, exportar PDF, salir
    resultado = subprocess.run(
        [sys.executable, "menu.py"],
        cwd=SRC_DIR,
        input=entrada_usuario,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "Reporte ejecutivo en PDF guardado en" in resultado.stdout

    ruta_pdf = os.path.join(SRC_DIR, "..", "output", "reporte_resumen.pdf")
    assert os.path.exists(ruta_pdf)


def test_menu_pdf_sin_auditoria_previa_no_lo_tumba():
    entrada_usuario = "7\n8\n"  # exportar PDF sin haber ejecutado auditoria
    resultado = subprocess.run(
        [sys.executable, "menu.py"],
        cwd=SRC_DIR,
        input=entrada_usuario,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert resultado.returncode == 0
    assert "Primero debes ejecutar la auditoria" in resultado.stdout
