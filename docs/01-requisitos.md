# SaludAudita — Requisitos (Fase 1: Definición y alcance)

## 1. Objetivo del proyecto
Herramienta de auditoría automática de facturación en salud (Python + Pandas + SQL),
construida como proyecto de portafolio para la pasantía del SENA (ADSO), a partir de
la experiencia real de +12 años del autor en auditoría y facturación en IPS y clínicas
colombianas.

## 2. Alcance del MVP (v2 — ampliado con base normativa)
El MVP detecta automáticamente 6 categorías de inconsistencias:

| # | Categoría | Regla base |
|---|---|---|
| 1 | Servicios/procedimientos sin soporte o autorización | `Tiene_Soporte = No` **o** `Tiene_Autorizacion = No` |
| 2 | Códigos CUPS/CIE10 inválidos o no autorizados | Código no existe en la tabla de referencia `CUPS_Validos` |
| 3 | Glosas repetidas o mal aplicadas | Misma glosa repetida en la misma factura, o glosa sin justificación en el servicio |
| 4 | Descuadres en totales/valores facturados | `Valor_Unitario × Cantidad ≠ Valor_Total_Registrado` |
| 5 | ✅ Devolución por radicación extemporánea | Más de 22 días hábiles entre `Fecha_Expedicion_Factura` y `Fecha_Radicacion_Soportes` |
| 6 | Descuadre contra el tarifario pactado | `Valor_Unitario ≠ Valor_Tarifario_Referencia` |

**Regla 5 — base normativa verificada:**
✅VERIFICADO — [Resolución 2284 de 2023, Ministerio de Salud y Protección
Social](https://www.minsalud.gov.co/Normatividad_Nuevo/Resoluci%C3%B3n%20No%202284%20de%202023.pdf)
(Manual Único de Devoluciones, Glosas y Respuestas), vigente desde el 1 de
octubre de 2024 (transitoriedad ajustada por la Resolución 627 de 2024):
establece como causal taxativa de devolución la no radicación de los
soportes dentro de los 22 días hábiles siguientes a la fecha de expedición
de la factura. La resolución también distingue formalmente **devolución**
(rechazo total, antes del trámite de pago) de **glosa** (observación de
valor, durante la auditoría) — de ahí que en el MVP ambos conceptos ahora
tengan reglas y columnas separadas.

⚠️ Limitación declarada: el conteo de días hábiles excluye sábados y
domingos, pero no festivos colombianos (no se implementó un calendario de
festivos en este MVP).

**Regla 6 — nota de transparencia:**
❓NO VERIFICABLE como tarifa oficial — `Valor_Tarifario_Referencia` es un
valor simulado en el dataset de prueba, no proviene de un tarifario SOAT/
ISS2001 real. En un caso real, esta columna se llenaría cruzando contra el
tarifario/contrato vigente con cada EPS.

## 3. Fuente de datos
- **MVP:** Excel/CSV simulado por el autor (no hay acceso a datos reales, ya que
  actualmente no está vinculado laboralmente).
- **Mejora futura (fuera del MVP):** adaptar a estructura RIPS real (requiere
  verificar la resolución/estructura oficial vigente antes de implementar).

## 4. Estructura de datos simulados (`data/facturas_simuladas.xlsx`)

| Columna | Descripción |
|---|---|
| N_Factura | Identificador de cada registro |
| Fecha_Servicio | Fecha en la que se prestó el servicio |
| Fecha_Expedicion_Factura | Fecha de expedición de la factura |
| Fecha_Radicacion_Soportes | Fecha en que se radicaron los soportes (para regla 5) |
| Codigo_CUPS | Código del procedimiento/servicio |
| Diagnostico_CIE10 | Código de diagnóstico (simulado, ver nota abajo) |
| Descripcion_Servicio | Descripción legible del servicio |
| Tiene_Soporte | Sí/No |
| Tiene_Autorizacion | Sí/No |
| N_Autorizacion | Número de autorización (si aplica) |
| Manual_Tarifario | SOAT / ISS2001 / Particular |
| Valor_Tarifario_Referencia | Valor de referencia del tarifario (simulado, para regla 6) |
| Valor_Unitario | Valor unitario del servicio |
| Cantidad | Cantidad de unidades prestadas |
| Valor_Total_Registrado | Valor total tal como quedó facturado |
| Valor_Total_Calculado | `Valor_Unitario × Cantidad` (fórmula) |
| Diferencia | `Valor_Total_Registrado − Valor_Total_Calculado` (fórmula) |
| Glosa_Aplicada | Glosa aplicada al registro, si existe |

Hoja adicional `CUPS_Validos`: tabla de referencia de códigos válidos, usada para
validar la categoría 2.

❓ Nota sobre `Diagnostico_CIE10`: los códigos usados en el dataset simulado
son ilustrativos (con formato real de CIE10), pero no están validados contra
la tabla oficial completa — se usan solo para dar contexto clínico simulado,
no para una regla de pertinencia diagnóstico-procedimiento en este MVP.

## 5. Fuera de alcance del MVP
- Estructura RIPS real
- Conexión a bases de datos externas o sistemas reales
- Interfaz gráfica (el MVP se valida por script/notebook, no por UI)

## 6. Notas de verificabilidad
- ❓ Las reglas de negocio anteriores son una base de trabajo propuesta y validada
  por el autor con base en su experiencia profesional; no citan una norma específica
  porque este MVP no pretende ser conforme a ninguna resolución oficial de RIPS/glosas.
  Esa conformidad queda como trabajo futuro, condicionado a revisar la normativa vigente.
