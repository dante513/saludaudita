# SaludAudita — Arquitectura (Fase 2: Diseño)

> 💭 Propuesta de arquitectura — a validar por el autor antes de pasar a desarrollo.

## 1. Enfoque general
Arquitectura modular en Python: un módulo independiente por cada regla de negocio,
orquestados por un módulo principal. Esto permite añadir o modificar reglas sin
tocar el resto del sistema (bajo acoplamiento).

## 2. Estructura de carpetas propuesta

```
saludaudita/
├── README.md
├── docs/
│   ├── 01-requisitos.md
│   ├── 02-arquitectura.md
│   └── 03-bitacora.md
├── data/
│   └── facturas_simuladas.xlsx
├── src/
│   ├── main.py                  # Orquestador: corre todas las validaciones y genera el reporte
│   ├── loaders.py                # Carga el Excel/CSV a un DataFrame de pandas
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── soporte_autorizacion.py   # Regla 1
│   │   ├── codigos_invalidos.py      # Regla 2
│   │   ├── glosas.py                 # Regla 3
│   │   └── totales.py                # Regla 4
│   └── report.py                 # Consolida hallazgos y exporta el reporte final
├── output/
│   └── reporte_hallazgos.xlsx    # Generado por el sistema (no se versiona)
└── tests/
    └── (fase de pruebas)
```

## 3. Flujo de datos (pipeline)

1. `loaders.py` lee `facturas_simuladas.xlsx` (hoja `Facturas` + hoja `CUPS_Validos`) → 2 DataFrames de pandas
2. `main.py` pasa esos DataFrames a cada validador de `validators/`
3. Cada validador devuelve las filas que incumplen su regla, con una columna `Motivo_Hallazgo`
4. `report.py` consolida todos los hallazgos en un solo DataFrame y lo exporta a
   `output/reporte_hallazgos.xlsx`, con una fila por hallazgo (una factura puede
   aparecer varias veces si incumple más de una regla)

## 4. Diseño de cada validador

| Módulo | Entrada | Lógica | Salida |
|---|---|---|---|
| `soporte_autorizacion.py` | df Facturas | `Tiene_Soporte == "No"` o `Tiene_Autorizacion == "No"` | filas + motivo |
| `codigos_invalidos.py` | df Facturas + df CUPS_Validos | `Codigo_CUPS` no está en la lista de códigos válidos | filas + motivo |
| `glosas.py` | df Facturas | glosa no vacía repetida en el mismo `N_Factura`, o glosa aplicada sin que exista la condición que la justifique | filas + motivo |
| `totales.py` | df Facturas | `abs(Diferencia) > 0` (tolerancia configurable, ej. $0) | filas + motivo |

## 5. Rol de SQL (según lo definido: Python + Pandas + SQL)
💭 Propuesta: SQL no reemplaza a pandas para las validaciones (pandas es más simple
para este volumen de datos), sino que se usa para:
- Persistir el dataset y los hallazgos en una base **SQLite** local (`saludaudita.db`),
  simulando cómo se vería en un sistema real con base de datos.
- La tabla `CUPS_Validos` vive como tabla SQL de referencia, y se consulta con una
  query (`SELECT Codigo_CUPS FROM cups_validos`) en vez de leerla solo del Excel.
- Esto le da al proyecto una capa de persistencia real, no solo procesamiento en
  memoria — valioso para el portafolio.

## 6. Convenciones de código
- Nombres de funciones en español, consistentes con el dominio (ej. `validar_soporte_autorizacion`)
- Cada validador recibe un DataFrame y retorna un DataFrame (nunca modifica el original)
- Sin hardcodear rutas de archivo — usar constantes al inicio de `main.py`

## 7. Decisiones confirmadas (2026-09-10)
- ✅ Persistencia: **SQLite** (archivo local `saludaudita.db`, sin servidor)
- ✅ Reporte final de hallazgos: se exporta en **ambos formatos**, `.xlsx` y `.csv`,
  en `output/reporte_hallazgos.xlsx` y `output/reporte_hallazgos.csv`
