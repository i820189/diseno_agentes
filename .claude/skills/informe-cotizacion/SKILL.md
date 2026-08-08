---
name: informe-cotizacion
description: Genera el informe/expediente de cotización que recibe el asesor comercial de "Tus Eventos" a partir de los datos de una conversación (evento, asistentes, fecha, zona, alternativa evaluada). Usa SOLO precios del catálogo semilla y marca supuestos. Es la especificación del payload de derivar_a_asesor.
---

# Informe de Cotización para el Asesor Comercial

Genera un expediente profesional en Markdown que el asesor humano pueda leer en
**menos de 1 minuto** para retomar la conversación sin repreguntar nada al cliente.
Refleja la estructura de derivación del **Agentic Profile Card v3.2 §3.2**: resumen
de lo conversado, datos recopilados, validaciones realizadas, alternativa evaluada
y motivo exacto de la derivación.

## Entradas

El usuario proporciona los datos en texto libre o pegando la conversación. Extraer:

- **Datos mínimos (4 slots obligatorios):** tipo de evento · nº de asistentes · fecha · ubicación/zona.
- **Opcionales:** presupuesto, preferencias, categorías de interés, datos de contacto (solo si el cliente los dio).
- **Alternativa(s) evaluada(s)** y por qué se recomendó una.
- **Motivo de la derivación** (descuento, excepción, pago, reclamo, pedido explícito, fallo de tool, etc.).

## Reglas (no negociables)

1. **Precios SOLO del catálogo** `conocimiento/catalogo-precios-semilla.json` (zona × temporada; +S/50 piso sin ascensor). Si un precio no está en el catálogo, escribir `PENDIENTE DE CATÁLOGO` — **jamás inventarlo**.
2. Todo dato no confirmado por el cliente se marca **(SUPUESTO)**; todo faltante va a la sección "Falta por confirmar". Nunca rellenar huecos en silencio.
3. **Validaciones**: reportar cada gate con ✅/❌/⚠️ — cobertura de zona, anticipación 72 h (feriados: entrega el día hábil anterior, recojo al día siguiente), capacidad, disponibilidad.
4. **PII mínima**: solo los datos de contacto que el cliente entregó voluntariamente; nada de datos de otros clientes.
5. Cerrar siempre con el **disclaimer**: *"Precios y disponibilidad referenciales, sujetos a confirmación. Vigencia: 72 horas."*
6. La cotización queda en estado **COTIZACIÓN (no bloquea disponibilidad)** — el informe recuerda al asesor que la conversión a reserva pendiente/confirmada es suya.

## Salida

Archivo `informes/INFORME-COT-<YYYYMMDD>-<cliente-o-alias>.md` (crear la carpeta si no existe) con esta plantilla:

```markdown
# 📋 Informe de Cotización — [alias cliente] · [fecha hora]
**Estado:** COTIZACIÓN (no bloquea disponibilidad) · **Vigencia:** 72 h · **Canal:** WhatsApp

## 1 · Resumen ejecutivo (3 líneas máx.)
[Qué busca el cliente, qué se le recomendó, en qué quedó la conversación.]

## 2 · Datos del evento
| Slot | Valor | Confirmado |
|---|---|---|
| Tipo de evento | … | ✅ / (SUPUESTO) |
| Asistentes | … | … |
| Fecha | … | … |
| Ubicación / zona | … | … |
| Presupuesto | … | … |
| Preferencias | … | … |

## 3 · Validaciones realizadas
- Cobertura de zona: ✅/❌ [detalle]
- Anticipación 72 h / feriados: ✅/❌ [detalle]
- Disponibilidad en fecha: ✅/⚠️ [detalle]
- Capacidad para N asistentes: ✅/❌ [detalle]

## 4 · Alternativa evaluada y cotización
[Alternativa recomendada + criterios (ocasión, capacidad, disponibilidad, presupuesto).]
| Concepto | Detalle | Precio (catálogo) |
|---|---|---|
| … | … | S/ … |
| Adicional piso sin ascensor | si aplica | S/ 50 |
| **Total referencial** | | **S/ …** |

## 5 · Falta por confirmar
- [ ] …

## 6 · Motivo de la derivación y siguiente paso sugerido
**Motivo:** [exacto — p. ej. "cliente pide descuento por 3 fechas"]
**Siguiente paso:** [p. ej. "llamar hoy antes de las 18h; convertir a reserva pendiente si acepta"]

---
*Precios y disponibilidad referenciales, sujetos a confirmación. Vigencia: 72 horas.*
*Generado por el flujo de derivación (spec de la tool `derivar_a_asesor` — Profile Card v3.2 §3.2).*
```

## Al terminar

Reportar en una línea: archivo generado, total referencial, nº de supuestos y nº de
pendientes — p. ej. `INFORME-COT-20260807-carla.md · S/ 1 250 · 2 supuestos · 1 pendiente`.
Si faltan los 4 slots obligatorios, decirlo y NO generar el total (igual que el gate del agente).
