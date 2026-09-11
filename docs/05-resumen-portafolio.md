# SaludAudita — Resumen de portafolio (Fase 6: Cierre)

## ¿Qué es?
Un auditor automático de facturación en salud construido en Python. Toma un
conjunto de facturas (Excel) y detecta automáticamente 6 tipos de
inconsistencias que normalmente se revisan a mano en auditoría de cuentas
médicas: falta de soporte/autorización, códigos CUPS inválidos, glosas mal
aplicadas, descuadres en los totales facturados, devolución por radicación
extemporánea (con base en la Resolución 2284 de 2023) y descuadre contra el
tarifario pactado.

## ¿De dónde sale la idea?
De experiencia real: más de 12 años trabajando en facturación y auditoría en
salud en IPS y clínicas colombianas (incluyendo Agost+ S.A.S., enero–julio
2026). Las 4 reglas de negocio del proyecto no son teóricas — son los errores
que más se repiten en la práctica.

## Stack técnico
- **Python** — lógica de negocio y orquestación
- **Pandas** — carga, limpieza y validación de datos
- **SQLite** — persistencia del dataset y de los hallazgos
- **openpyxl** — lectura/escritura de Excel con fórmulas reales
- **pytest** — pruebas automatizadas

## Resultados verificables
> ✅ VERIFICADO por ejecución directa en este proyecto (no son cifras de
> referencia externa, son las obtenidas al correr el código):

| Métrica | Valor |
|---|---|
| Facturas simuladas analizadas | 31 |
| Hallazgos totales detectados | 28 |
| Pruebas automatizadas | 47 / 47 pasando |
| Categorías de reglas de negocio | 6 (2 con base en la Resolución 2284 de 2023) |
| Formatos de salida del reporte | Excel (.xlsx), CSV y PDF ejecutivo |
| Interfaces disponibles | Menú de consola y aplicación web (Streamlit) |
| Historial de auditorías | SQLite, acumulativo (append), con tolerancias usadas en cada corrida |

## Cómo se construyó (metodología)
Cascada adaptada por fases, con checkpoints:
1. Definición y alcance
2. Diseño de arquitectura
3. Desarrollo modular (un archivo por regla de negocio)
4. Pruebas automatizadas (pytest)
5. Documentación (este set de documentos + diagrama de arquitectura)
6. Cierre / portafolio (este documento)

Ver el detalle de cada fase en `docs/01-requisitos.md`, `docs/02-arquitectura.md`
y `docs/03-bitacora.md`.

## Limitaciones actuales (transparencia, no se ocultan)
- ❓ Usa datos **simulados**, no reales — por no tener acceso a datos de un
  empleador actual. Las reglas de negocio están inspiradas en experiencia real,
  pero el dataset en sí es ficticio.
- ❓ No implementa la estructura RIPS oficial — queda como mejora futura,
  condicionada a revisar la normativa vigente antes de implementarla.
- La interfaz es de consola (menú interactivo), no gráfica.

## Próximos pasos posibles (fuera del MVP actual)
- Migrar el dataset simulado a estructura RIPS real
- Agregar más reglas de negocio con base en más casos reales
- Explorar una interfaz gráfica simple si el tiempo lo permite
