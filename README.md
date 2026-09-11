# SaludAudita

Auditor/validador automático de facturación en salud, construido con Python,
Pandas y SQL. Proyecto de portafolio (SENA - ADSO), basado en experiencia real
de +12 años en auditoría y facturación en el sector salud colombiano.

## Estado actual
✅ Fases 1 a 6 completas — MVP funcional, probado, documentado y listo para portafolio

## Documentación
- `docs/01-requisitos.md` — alcance y reglas de negocio
- `docs/02-arquitectura.md` — diseño técnico
- `docs/03-bitacora.md` — registro de avances por fecha
- `docs/04-diagrama-arquitectura.svg` — diagrama visual del pipeline
- `docs/05-resumen-portafolio.md` — resumen ejecutivo para presentar el proyecto

## Cómo ejecutarlo

**Para compartir con alguien más (recomendado):**
Comparte toda la carpeta `saludaudita` y dile que haga doble clic en
`iniciar.bat`. Ese archivo instala solo lo necesario (la primera vez que se
usa) y abre la aplicación en el navegador — no requiere escribir ningún
comando. Sí necesita tener Python instalado en su computador (si no lo tiene,
el propio lanzador se lo indica con un mensaje).

**Para uso propio, desde la terminal:**
```
cd src
pip install -r ../requirements.txt
streamlit run app.py
```
Se abre en el navegador. Puedes subir un Excel propio o usar el simulado por
defecto, ajustar las tolerancias de descuadre, ejecutar la auditoría,
filtrar los hallazgos por regla o número de factura, ver reincidencias, y
descargar el reporte en Excel, CSV o PDF ejecutivo directamente desde ahí.

**Opción alterna — menú de consola:**
```
cd src
python menu.py
```

Para correr solo el análisis sin ninguna interfaz (modo script):
```
cd src
python main.py
```

## Metodología
Cascada adaptada por fases, con checkpoints:
Definición y alcance → Diseño → Desarrollo por módulos → Pruebas →
Documentación final → Cierre / portafolio

## Estructura del proyecto
```
saludaudita/
├── README.md
├── iniciar.bat               # Doble clic para compartir sin comandos manuales
├── requirements.txt           # Dependencias del proyecto
├── docs/
│   ├── 01-requisitos.md     # Alcance y reglas de negocio
│   ├── 02-arquitectura.md   # Diseño técnico
│   └── 03-bitacora.md       # Registro de avances por fecha
├── data/
│   └── facturas_simuladas.xlsx   # Dataset simulado para pruebas
├── src/
│   ├── main.py                # Orquestador: expone ejecutar_auditoria() y modo script
│   ├── menu.py                 # Menu interactivo por consola
│   ├── app.py                  # Interfaz web (Streamlit) - opcion recomendada
│   ├── loaders.py              # Carga el Excel a DataFrames de pandas
│   ├── validators/           # Un módulo por regla de negocio
│   ├── report.py             # Consolida hallazgos y exporta el reporte
│   └── db.py                 # Persistencia en SQLite
├── output/                   # Reportes generados (no se versiona)
└── tests/                    # 21 pruebas automáticas (pytest)
```

## Aviso sobre los datos
Todos los datos en `data/facturas_simuladas.xlsx` son **100% ficticios**,
generados para fines de prueba y portafolio. No contienen información real
de pacientes, IPS ni EPS.
