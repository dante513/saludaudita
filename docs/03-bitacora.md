# Bitácora de avances — SaludAudita

## 2026-09-10
- Definida la metodología de trabajo: cascada adaptada por fases con checkpoints.
- Cerrado el alcance del MVP: 4 categorías de inconsistencias (soporte/autorización,
  CUPS/CIE10 inválido, glosas mal aplicadas, descuadres de totales).
- Decidida la fuente de datos del MVP: Excel simulado (sin acceso a datos reales
  por no estar vinculado laboralmente actualmente).
- Creada la estructura de carpetas del proyecto y el documento de requisitos
  (`docs/01-requisitos.md`).
- Generado el dataset simulado (`data/facturas_simuladas.xlsx`) con casos válidos
  y casos con errores intencionales de las 4 categorías.
- Cerrada la fase 2 (arquitectura): SQLite para persistencia, reporte en .xlsx y .csv.
- Fase 3 (desarrollo) — primer avance funcional de punta a punta:
  - `src/loaders.py`, `src/validators/` (4 reglas), `src/report.py`, `src/db.py`, `src/main.py`
  - Ejecutado sobre las 31 facturas simuladas: 21 hallazgos totales
    (11 sin soporte/autorización, 5 glosa mal aplicada, 3 código inválido, 2 descuadre)
  - ⚠️ Detectado durante desarrollo: `Codigo_CUPS` podía perder ceros a la izquierda
    al leerse desde Excel (ej. "000000" se leía como "0").

## 2026-09-10 (continuación) — Fase 4: Pruebas
- ✅ Corregido `loaders.py`: se fuerza `dtype={"Codigo_CUPS": str}` al leer el Excel,
  para no perder ceros a la izquierda.
- Creada la suite de pruebas en `tests/` (pytest): 19 pruebas — 5 por cada uno de los
  4 validadores + 1 de integración sobre el dataset completo. **19/19 pasaron.**
- Nota de documentación para quien consuma `output/reporte_hallazgos.xlsx`/`.csv`:
  el archivo guarda `Codigo_CUPS` correctamente como texto (verificado con
  `openpyxl`, `data_type='s'`); si se vuelve a leer con pandas sin `dtype=str`,
  pandas puede reinterpretar códigos como "000000" como el número 0. No es un
  defecto del reporte, es responsabilidad de quien lo consuma después.
- Agregado `src/menu.py`: menú interactivo por consola (ejecutar auditoría,
  ver resumen por regla, ver detalle de una regla, buscar por N° de factura).
  `main.py` se refactorizó exponiendo `ejecutar_auditoria()` para que tanto el
  modo script como el menú lo reutilicen.
- Agregadas 2 pruebas más para el menú (via `subprocess`, simulando entrada de
  usuario). **Total: 21/21 pruebas pasando.**
- ✅ Confirmado por el autor: el menú corre correctamente en su propio
  computador (Windows, Python 3.14.3), con los mismos resultados obtenidos en
  las pruebas (31 facturas, 21 hallazgos).

## 2026-09-10 (cierre) — Fases 5 y 6
- Fase 5 (documentación): creado `docs/04-diagrama-arquitectura.svg` con el
  flujo completo del pipeline (Excel → loaders → 4 validadores → report/db →
  output), y README actualizado enlazando toda la documentación.
- Fase 6 (cierre/portafolio): creado `docs/05-resumen-portafolio.md` con
  resumen ejecutivo, stack técnico, métricas verificadas por ejecución directa,
  y limitaciones actuales declaradas de forma transparente (dataset simulado,
  sin estructura RIPS real, interfaz solo de consola).
- **Proyecto cerrado como MVP completo: fases 1–6 terminadas en una sola
  sesión de trabajo.**

## 2026-09-10 (continuación) — Interfaz web con Streamlit
- Decisión: en vez de depender solo del menú de consola (poco práctico para
  compartir con un compañero o en una empresa), se agregó `src/app.py`, una
  interfaz web con Streamlit que reutiliza los mismos módulos de `loaders.py`,
  `validators/` y `report.py`.
- Funcionalidad: subir un Excel propio (o usar el simulado por defecto),
  ejecutar la auditoría, ver métricas y gráfico de hallazgos por regla,
  filtrar por regla/factura, y descargar el reporte en Excel o CSV.
- ✅ Verificado: la app levanta correctamente (HTTP 200, sin errores en el
  log de Streamlit).
- Alternativas evaluadas: ejecutable .exe con PyInstaller e interfaz de
  escritorio con Tkinter — quedan como posibles pasos futuros de mayor
  nivel de "cero instalación".

## 2026-09-10 (continuación) — Lanzador sin comandos manuales
- Agregados `requirements.txt` y `iniciar.bat`: la persona que reciba la
  carpeta solo hace doble clic en `iniciar.bat` — el script verifica que
  tenga Python (avisa con instrucciones claras si no lo tiene), instala
  las dependencias en silencio y abre la app en el navegador. Cero comandos
  manuales para quien lo recibe.
- Pendiente (fuera del alcance de este entorno de trabajo): generar un .exe
  standalone con PyInstaller para eliminar incluso la necesidad de tener
  Python instalado. Debe generarse en un Windows real, no desde este
  entorno Linux — queda como siguiente paso si se necesita ese nivel.

## 2026-09-10 (continuación) — v2: reglas basadas en normativa real
- Investigada la normativa vigente (búsqueda web, no memoria): Resolución
  2284 de 2023 del Ministerio de Salud (Manual Único de Devoluciones, Glosas
  y Respuestas), vigente desde el 1 de octubre de 2024. Confirma la
  distinción formal entre devolución y glosa, y una causal taxativa concreta:
  radicación de soportes fuera de 22 días hábiles desde la expedición.
- Agregadas 5 columnas nuevas al dataset: `Fecha_Expedicion_Factura`,
  `Fecha_Radicacion_Soportes`, `Diagnostico_CIE10`, `Manual_Tarifario`,
  `Valor_Tarifario_Referencia`.
- Agregadas 2 reglas nuevas: `validators/devolucion_radicacion.py` (regla 5,
  con base normativa real) y `validators/descuadre_tarifario.py` (regla 6,
  con valores de referencia simulados, declarado como tal).
- ⚠️ Detectado y corregido un error de diseño antes de presentarlo como
  resultado: la primera versión de `Valor_Tarifario_Referencia` se generaba
  multiplicando el valor unitario por un factor fijo según el tipo de
  tarifario, lo que marcaba como "descuadre" al 21 de 31 facturas (ruido de
  diseño, no error real simulado). Corregido para que el valor coincida por
  defecto y solo se fuerce un descuadre en los casos de prueba intencionales.
- Suite de pruebas ampliada a **29/29 pasando** (4 nuevas para regla 5,
  incluyendo un caso límite exacto de 22 vs 23 días hábiles calculado con
  `numpy.busday_count`; 4 nuevas para regla 6).
- Resultado verificado tras la corrección, corriendo el pipeline completo:
  **31 facturas, 28 hallazgos** (6: sin soporte/autorización, 5: glosa mal
  aplicada, 2: descuadre de totales, 5: radicación extemporánea,
  3: código inválido, 7: descuadre tarifario).
- Confirmado que la app de Streamlit sigue funcionando sin errores con las
  columnas y reglas nuevas (HTTP 200, log limpio).

## 2026-09-10 (continuación) — Afinamientos: tolerancias e historial
- **Tolerancias configurables desde la interfaz**: `app.py` ahora tiene
  campos numéricos para ajustar la tolerancia de descuadre de totales y de
  descuadre tarifario, en vez de tenerla fija en $0. Se pasan a
  `validar_totales(tolerancia=...)` y `validar_descuadre_tarifario(tolerancia=...)`.
- **Historial de auditorías en SQLite**: agregada `guardar_historial_auditoria()`
  en `db.py`, que hace `append` (no `replace`) a la tabla
  `historial_auditorias`, con fecha/hora y las tolerancias usadas en cada
  corrida. Agregada `obtener_resumen_historial()` para consultarlo agrupado
  por fecha y regla. Disponible tanto en `menu.py` (opción 5) como en
  `app.py` (sección expandible). `app.py` ahora también persiste en SQLite
  (antes no lo hacía).
- ✅ Verificado con ejecución real (no solo con pruebas unitarias): se corrió
  la auditoría 4 veces seguidas y las 4 corridas quedaron acumuladas en el
  historial con timestamps distintos, confirmando que es un `append` real.
- Suite de pruebas ampliada a **34/34 pasando**, incluyendo pruebas directas
  de `db.py` con una base SQLite en memoria (`test_db_historial.py`).

## 2026-09-10 (continuación) — Reporte de reincidencias
- Agregado `src/analisis.py`: `top_facturas_reincidentes()` (facturas con 2 o
  más hallazgos, con cuántas reglas distintas) y
  `top_codigos_cups_reincidentes()` (códigos CUPS repetidos en 2 o más
  facturas distintas). No agrega reglas de negocio nuevas — solo agrupa los
  hallazgos ya generados para priorizar revisión manual.
- Disponible en `menu.py` (nueva opción 6, "Salir" pasó a ser la 7) y en
  `app.py` (sección "Reincidencias" con las dos tablas lado a lado).
- ✅ Verificado sobre el dataset real: FAC-1005 es la única factura con 4
  hallazgos en 2 reglas distintas (por el caso de glosa repetida que se
  diseñó intencionalmente); el código CUPS 890301 es el más repetido, con
  6 hallazgos en 6 facturas distintas.
- Suite de pruebas ampliada a **41/41 pasando**.

## 2026-09-10 (continuación) — Reporte ejecutivo en PDF
- Agregado `src/pdf_report.py` (con `reportlab`, siguiendo la guía del skill
  de PDF del entorno de trabajo — Platypus, sin caracteres Unicode de sub/
  superíndice): genera un PDF de 2 páginas con métricas, hallazgos por
  regla, las 2 tablas de reincidencias, y el detalle de hallazgos
  (limitado a 60 filas para no volverse enorme; el detalle completo sigue
  disponible en el .xlsx/.csv).
- Disponible en `menu.py` (nueva opción 7, "Salir" pasó a ser la 8) y en
  `app.py` (botón de descarga junto a CSV y Excel, generado en memoria con
  `io.BytesIO`, sin tocar disco).
- ✅ Verificado abriendo el PDF real con `pdfplumber` y comparando el texto
  extraído contra los números ya conocidos (31 facturas, 28 hallazgos, 6
  reglas, FAC-1005 como reincidente) — no solo se confirmó que el archivo
  se creaba, se confirmó que el contenido es correcto.
- Suite de pruebas ampliada a **47/47 pasando**, incluyendo 4 pruebas nuevas
  que abren el PDF generado y verifican su contenido (métricas, reincidencia,
  dataset vacío, tolerancias reflejadas en el encabezado).
- Con esto se completaron las 4 ideas de afinamiento propuestas: tolerancias
  configurables, historial en SQLite, reincidencias, y reporte en PDF.
