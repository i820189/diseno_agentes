# Agentic Profile Card

## Agente de recomendaciones y atención para ocasiones de consumo ("Tus Eventos")

**Versión:** 12 de octubre de 2026 — alineada al código de la rama principal (commit bf7be53)
**Arquitectura:** Workflow en LangGraph de seis pasos con un agente decisor acotado (LLM aumentado + encadenamiento de pasos + enrutamiento, según *Building effective agents* de Anthropic)
**Canal actual:** Web Chat (Streamlit) sobre una API; WhatsApp previsto con el mismo backend
**Autonomía:** Semiautónomo y constreñido
**Criticidad:** Media-Alta controlada

Cambios respecto a la v3.2 (agosto): el agente ya existe y está desplegado; se documenta lo que hace hoy (catálogo de bebidas y servicios para eventos en Lima, 13 herramientas, memoria en Redis y PostgreSQL, guardrails en cinco capas, evals y red teaming) y se marcan como **previstos** los puntos de la v3.2 que aún no están en el código (WhatsApp, seguimientos automáticos, preferencias con consentimiento, motor de comparación por pesos).

---

# 1. Communication Layer

## Conversacional

El agente atiende por **Web Chat** (interfaz Streamlit que llama a la API del backend). En cada turno identifica la intención del cliente entre dieciséis posibles (saludo, nueva cotización, retomar previa, consulta de memoria, imagen, cierre, derivación, descuento, pago, cotización, consulta de precio, confirmación de derivación, revisar pedido, modificar pedido, consulta general y recomendación), extrae los datos del evento que vengan en el mensaje, pide únicamente lo que falta, muestra el catálogo aplicable, propone cantidades dimensionadas, emite la cotización y, cuando corresponde, deriva a un asesor. Habla en español, en mensajes cortos, y entrega artefactos: la cotización con su detalle y una imagen del evento cotizado.

**Previsto:** WhatsApp Business sobre el mismo backend, sin cambiar el agente.

## No conversacional

Hoy el agente ejecuta dos acciones fuera del diálogo: **retomar una cotización anterior** cuando el cliente se identifica con el mismo teléfono o correo (memoria de largo plazo) y **preparar la derivación** a un asesor con un resumen del caso y un enlace de WhatsApp. **Previsto:** recordatorios de vigencia de la cotización y seguimientos autorizados por el cliente.

---

# 2. Context Definition

## 2.1 Domain Definition

El agente pertenece al dominio de **atención comercial inicial para reuniones, celebraciones y eventos**: bebidas (cerveza, vino, ron, gaseosa, agua, hielo), servicio de bartender y paquetes como el bar móvil, para eventos en Lima (matrimonios, cumpleaños, reuniones, corporativos, aniversarios).

Acompaña al cliente desde su necesidad hasta una cotización sustentada considerando tipo de evento, cantidad de asistentes, fecha, distrito, productos pedidos, cobertura, calendario, stock y reglas del negocio. No reemplaza al asesor comercial: resuelve la atención inicial y entrega el caso listo para una posible intervención humana.

## 2.2 Objectives Definition

Guiar al cliente durante la selección, recomendar la opción más adecuada, recopilar la información necesaria y terminar en uno de tres resultados:

- **Recomendación explicable:** la alternativa que mejor se ajusta a la ocasión, con las validaciones realizadas a la vista (cobertura, catálogo, stock, fuente de la propuesta).
- **Cotización verificada:** detalle por producto, subtotal, IGV 18 %, total, vigencia de 48 horas y condiciones, con todos los importes tomados de la herramienta de precios.
- **Derivación a un asesor:** cuando el cliente lo pide explícitamente o cuando el caso exige negociar, aprobar una excepción, confirmar un pago o resolver algo fuera de su alcance.

Regla rectora: **el modelo decide qué hacer después, pero no puede saltarse una validación ni producir un número.**

---

# 3. Environment Definition

## 3.1 Knowledge

Todo el conocimiento proviene de fuentes oficiales del negocio, hoy en PostgreSQL (Cloud SQL) con una alternativa de datos de prueba para pruebas y evals:

- **Catálogo comercial:** productos con precio unitario y unidad, paquetes con precio base, aforo mínimo y máximo, tipos de evento compatibles, afinidad por ocasión y productos incluidos; alternativas por categoría.
- **Cobertura:** distritos atendidos (hoy seis; ampliación a Lima Metropolitana por UBIGEO en curso).
- **Disponibilidad:** stock de productos por fecha y cupos de paquetes por fecha.
- **Calendario:** reservas de eventos por fecha y distrito y capacidad diaria configurable.
- **Parámetros:** anticipación mínima de 72 horas, IGV 18 %, vigencia de la cotización de 48 horas; en feriados se entrega el día hábil anterior y se recoge al día siguiente.
- **Base de conocimiento de políticas:** condiciones del servicio y preguntas frecuentes en fragmentos con embeddings (pgvector), consultados solo cuando el cliente pregunta por el servicio.

El agente usa solo información oficial del catálogo y de la base de conocimiento; no debe completar estos datos con el conocimiento general del modelo.

## 3.2 Tools

Trece herramientas determinísticas, agrupadas por propósito. El decisor elige la acción; la herramienta consulta la fuente y devuelve el resultado.

**Comprender**

- **Clasificador de intención:** etiqueta el mensaje con una de las dieciséis intenciones, con confianza y evidencia; si la confianza es baja o el modelo falla, deciden las reglas.
- **Extractor de campos:** evento, fecha, asistentes, distrito, nombre, contacto y productos; reglas primero, modelo para lo que falta, siempre con salida estructurada.

**Validar**

- **Cobertura:** confirma que el distrito se atiende; si no, lo dice y lista los distritos cubiertos.
- **Calendario:** verifica reservas existentes para la fecha y el distrito contra la capacidad diaria.
- **Disponibilidad y stock:** cupos de paquetes y stock de productos para la fecha; propone reemplazos por categoría cuando falta.

**Proponer**

- **Catálogo:** paquetes y productos compatibles con el tipo de evento y el aforo; detecta productos pedidos que no existen en el catálogo.
- **Dimensionamiento:** cantidades por asistente según el tamaño del evento (bebidas, hielo, bartenders).
- **Precios y cotización:** subtotal, IGV, total y vigencia; registra la cotización como reserva en el calendario.

**Explicar**

- **Precio informativo:** precio unitario de un producto sin generar cotización ni reservar stock.
- **Base de conocimiento (RAG) de políticas:** recupera los fragmentos relevantes y responde solo con ese contexto. *El código aplica las reglas; el RAG las explica.*

**Cerrar y recordar**

- **Derivación a asesor:** resumen del caso y enlace de WhatsApp; solo si el cliente lo pide.
- **Imagen del evento:** tarjeta visual de la cotización.
- **Memoria:** sesión activa y cotizaciones previas por contacto.

**Previsto (v3.2, aún no en el código):** motor de comparación con pesos configurables por el negocio y conexión a un CRM para la derivación.

## 3.3 Short-Term Memory

La sesión activa se guarda en **Redis** con vencimiento de 24 horas (archivo local en pruebas) y contiene: identificador de sesión y etapa del flujo; intención del turno; tipo de evento, asistentes, fecha (o fecha parcial), distrito, nombre y contacto; productos pedidos y productos no soportados; campos faltantes; validaciones realizadas (cobertura, calendario, disponibilidad); opción recomendada y dimensionamiento; cotización emitida; derivación y su resumen; historial de mensajes y trazas por nodo.

Esta memoria evita repreguntar y permite modificar el pedido (cambiar o reemplazar productos, fecha o distrito) sin perder lo validado.

## 3.4 Long-Term Memory

En **PostgreSQL** (documento JSON por contacto) se conservan las cotizaciones previas: cuando el cliente vuelve e indica el mismo teléfono o correo, el agente ofrece retomar la última cotización o empezar una nueva. **Previsto:** preferencias guardadas solo con consentimiento explícito, consultables y eliminables por el cliente.

---

# 4. Autonomy Dimension Definition

## Nivel de autonomía: Semiautónomo y constreñido

El agente puede comprender la solicitud, pedir datos faltantes, consultar las fuentes del negocio, validar condiciones, proponer una alternativa dimensionada, emitir una cotización verificada, mostrar su imagen, responder precios y políticas, retomar una cotización previa y preparar una derivación.

La autonomía está en un solo punto, el decisor, y es validada: elige una de diez acciones permitidas (pedir campos faltantes, validar y recomendar, generar cotización, responder precio, responder política, mostrar imagen, derivar, retomar previa, nueva cotización, cierre) y un guardrail de decisión corrige cualquier elección que no cumpla los requisitos.

El agente no puede: aprobar descuentos; negociar excepciones; modificar precios; confirmar pagos; cerrar una venta; inventar disponibilidad o precios; cotizar sin cobertura, calendario y stock validados; derivar sin pedido explícito; mostrar imagen sin cotización; acceder a herramientas no registradas. Si el modelo no responde, el flujo degrada a reglas determinísticas en vez de caerse.

---

# 5. Criticality Dimension Definition

## Nivel de criticidad: Media-Alta controlada

Interviene en una decisión comercial, procesa datos de contacto, registra reservas y vende bebidas alcohólicas. Un error puede producir una promesa incumplible, una pérdida económica, una mala experiencia, un uso indebido de datos personales o una venta inadecuada.

## 5.1 Risks

- **Cotización con datos incompletos.** Mitigado: compuerta de datos mínimos (evento, asistentes, fecha, distrito, contacto, productos).
- **Cantidades mal dimensionadas.** Mitigado: dimensionamiento por reglas; limitación conocida: no hay tope de alcohol por asistente (en implementación).
- **Recursos no disponibles.** Mitigado: calendario y stock por fecha; limitación conocida: una cotización se registra como reserva confirmada y puede bloquear la fecha a otros (corrección en curso: reserva tentativa con vencimiento).
- **Precio incorrecto o inventado.** Mitigado: el modelo no calcula importes; los evals verifican el total.
- **Evento fuera de cobertura.** Mitigado: validación temprana de distrito; limitación conocida: cobertura de seis distritos y extracción de distrito frágil ("en Ate, cerveza"), ampliación por UBIGEO en curso.
- **Fechas relativas mal interpretadas** ("la próxima semana"). Limitación conocida, corrección en curso.
- **Datos de clientes expuestos.** Mitigado: sesiones aisladas por identificador con vencimiento; tarjetas enmascaradas; claves bloqueadas.
- **Acciones comerciales no autorizadas.** Mitigado: lista cerrada de acciones y guardrail de decisión.
- **Manipulación por mensajes maliciosos.** Mitigado: guardrails de entrada determinístico y semántico; red teaming en cada versión.
- **Fallo de sistemas.** Mitigado parcialmente: degradación a reglas si el modelo falla; limitación conocida: la consulta a la base de conocimiento sin conexión termina en error (respaldo en curso).
- **Latencia y costo.** Limitación conocida: con el modelo activo el decisor puede repetir llamadas; corrección en curso.
- **Venta a menores y consumo excesivo.** Control de edad (18+) al inicio y mensajes de consumo responsable en implementación (Ley N.º 28681).

## 5.2 Guardrails, Evals and Controls

### Guardrails en cinco capas

1. **Entrada determinística:** mensaje vacío, temas claramente ajenos al servicio (internet, recetas, programación, clima, noticias), intentos directos de cambiar reglas o revelar instrucciones. Respuesta segura fija sin llegar al modelo.
2. **Entrada semántica (LLM):** casos ambiguos: lenguaje de odio, discriminación, amenazas, contenido sexual o violento, extracción de datos sensibles, manipulación sutil, fuera de alcance no evidente. Nueve categorías con confianza; bloquea solo con confianza alta; ante la duda permite.
3. **Datos personales hacia el modelo:** nombre, teléfono y correo permitidos (son datos de contacto necesarios); tarjetas enmascaradas; claves de API bloqueadas.
4. **Decisión:** no cotiza sin requisitos, no muestra imagen sin cotización, no deriva sin pedido explícito, no altera precios por un descuento pedido en el chat.
5. **Salida:** evita respuestas vacías y derivaciones no solicitadas; persiste el estado validado.

### Controles de negocio

- Datos mínimos obligatorios antes de recomendar; solo se pregunta lo que falta.
- Solo alternativas activas del catálogo oficial; productos inexistentes se señalan y se ofrece reemplazo.
- Todo precio sale de la herramienta de precios con moneda, subtotal, IGV, total, vigencia y condiciones ("precio referencial, sujeto a disponibilidad y confirmación final").
- Cobertura, calendario y stock validados antes de recomendar o cotizar; una opción que no cumpla se descarta.
- Derivación obligatoria para descuentos, excepciones, pagos, confirmación de compra, reclamos y solicitud explícita de atención humana.
- Trazas por turno (nodo, decisión, herramientas, guardrails) y, con el modelo activo, trazas en LangSmith con tokens y latencia.

### Controles éticos

- Control de edad al inicio ("¿Tienes 18 años o más?"); bloqueo si el cliente declara ser menor. Verificación final en el asesor al concretar la venta.
- Consumo responsable: agua en el dimensionamiento para alternar con bebidas alcohólicas, advertencia "Tomar bebidas alcohólicas en exceso es dañino. Si bebes, no manejes" en la cotización, sin sobredimensionar alcohol para el aforo.
- Transparencia: el cliente sabe que conversa con un asistente automatizado y puede pedir un asesor en cualquier momento.
- Datos personales conforme a la Ley N.º 29733; principios de la Ley N.º 31814 (ética, transparencia, supervisión humana).

### Evaluaciones

- **72 pruebas automatizadas** (66 aprobadas, 6 omitidas por requerir PostgreSQL o Redis reales): extracción, datos faltantes, cobertura, fechas, cotización tras recomendación, descuentos sin efecto en precios, stock, calendario, memoria y repositorios.
- **7 evals de conversación completa** (estado final y respuesta): 7 de 7 en modo determinístico; 5 de 7 con el modelo activo (2 sin terminar por latencia).
- **Red teaming** con DeepTeam: 24 ataques en septiembre (versión original 5 fallos → versión reforzada 0) y campaña OWASP del 12 de octubre sobre la versión final (8 de 8 casos aprobados); prueba de humo de guardrails 6 de 9.
- **Métricas propuestas para producción:** exactitud de precios y disponibilidad, precisión de extracción por campo, derivaciones no solicitadas = 0, calidad del RAG (faithfulness, context precision), latencia y costo por turno, tiempo a la primera cotización y conversión.

---

# 6. Flujo de un turno

```text
MENSAJE DEL CLIENTE
        ↓
1. VALIDAR ENTRADA (guardrail determinístico + semántico) ──bloqueado──▶ respuesta segura
        ↓
2. CLASIFICAR INTENCIÓN Y EXTRAER CAMPOS (modelo + reglas)
        ↓
3. GESTIONAR MEMORIA (¿hay cotización previa de este contacto?) ──resuelve──▶ respuesta
        ↓
4. DECIDIR ACCIÓN (decisor: 1 de 10) → GUARDRAIL DE DECISIÓN
        ↓
5. EJECUTAR HERRAMIENTAS: cobertura → calendario → catálogo → stock → dimensionar → precios
   (o precio informativo · políticas vía RAG · imagen · derivación)
        ↓
6. EVALUAR SALIDA Y PERSISTIR (Redis + memoria larga)
        ↓
RECOMENDACIÓN EXPLICABLE · COTIZACIÓN VERIFICADA · DERIVACIÓN A ASESOR
```

---

# 7. Resumen para la imagen del Profile Card

**Communication Layer.** Conversacional: Web Chat (Streamlit + API) que identifica la intención, pide solo lo que falta, muestra catálogo, propone, cotiza y deriva; artefactos de cotización e imagen. WhatsApp previsto. No conversacional: retomar cotización previa por contacto y preparar la derivación con resumen.

**Domain Definition.** Atención comercial inicial de bebidas y servicios para reuniones, celebraciones y eventos en Lima. Acompaña al cliente hasta una recomendación, cotización o derivación válida; no reemplaza al asesor.

**Objectives Definition.** Comprender la intención, recopilar los datos indispensables, validar cobertura, calendario y stock, y terminar en una recomendación explicable, una cotización verificada (IGV 18 %, vigencia 48 h) o una derivación a un asesor.

**Knowledge.** Catálogo de productos y paquetes con aforo; cobertura por distrito; stock y cupos por fecha; calendario de reservas; parámetros (72 h, IGV, vigencia); base de conocimiento de políticas (RAG). Solo información oficial.

**Tools.** Clasificador e extractor · cobertura · calendario · disponibilidad y stock · catálogo · dimensionamiento · precios y cotización · precio informativo · RAG de políticas · derivación · imagen · memoria.

**Short-Term Memory.** Sesión en Redis (24 h): datos del evento y del cliente, productos, faltantes, validaciones, recomendación, cotización, derivación, etapa y trazas.

**Long-Term Memory.** Cotizaciones previas por contacto en PostgreSQL para retomar; preferencias con consentimiento previstas.

**Decision Making.** Seis pasos fijos; el decisor elige una de diez acciones y el guardrail de decisión la valida; degrada a reglas si el modelo falla.

**Guardrails.** Cinco capas: entrada determinística, entrada semántica con LLM, datos personales hacia el modelo, decisión y salida; más controles éticos de edad y consumo responsable.

**Evaluation.** 66 pruebas, 7 evals (7/7 y 5/7), red teaming DeepTeam (24 ataques: 5 → 0) y campaña OWASP (8/8), trazas en LangSmith.

**Autonomy.** Semiautónomo y constreñido: recomienda, cotiza y deriva; no negocia, no aprueba descuentos, no confirma pagos ni cierra ventas.

**Criticality.** Media-Alta controlada: riesgos de precio, cobertura, disponibilidad, datos personales, manipulación, venta de alcohol; controles de validación previa, fuentes oficiales, reglas determinísticas, guardrails, trazabilidad y supervisión humana.
