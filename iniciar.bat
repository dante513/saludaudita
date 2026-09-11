@echo off
setlocal

echo ================================================
echo   SaludAudita - Auditor de facturacion en salud
echo ================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo No se encontro Python instalado en este computador.
    echo.
    echo Para usar SaludAudita, primero instala Python desde:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: durante la instalacion, marca la casilla
    echo "Add Python to PATH" antes de darle a Instalar.
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0src"

echo Verificando/instalando lo necesario ^(solo tarda la primera vez^)...
python -m pip install --quiet --disable-pip-version-check -r ..\requirements.txt

if errorlevel 1 (
    echo.
    echo Hubo un problema instalando las dependencias.
    echo Revisa tu conexion a internet e intenta de nuevo.
    pause
    exit /b 1
)

echo.
echo Abriendo SaludAudita en el navegador...
echo ^(para cerrarlo, vuelve a esta ventana y presiona Ctrl+C^)
echo.

streamlit run app.py

pause
