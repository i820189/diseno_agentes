# Tarea S14 — Arquitectura de Solución "Tus Eventos" (GRUPAL · 20 pts · due JUE 7-AGO 11:59pm)

> **Entrega en Classroom = 2 partes:** ① la **caja de texto** con el sustento (abajo, listo para pegar) · ② el **archivo** del diagrama: adjuntar `arquitectura-tus-eventos.png` (ya exportada en esta carpeta) o el `.drawio` (Boris acepta el XML directo).
> **Criterio de Boris:** *"en base a eso [el sustento] debería yo ver LO MISMO en su arquitectura"* — por eso este doc mapea cada afirmación a una caja del diagrama.
> Basado en el **Profile Card v3.2 del equipo** (`profile-card/grupal/Profile_Card_Agente_Recomendaciones_Ocasiones_Consumo_v3.2.md`) y validado con los datos reales del negocio (Fernando).

---

## 1 · SUSTENTO — para debatir en equipo (y luego sintetizar)

**🎯 La tesis en una línea:**
> "Tus Eventos" es un **AGENTE ÚNICO** (Goal-Based + ReAct) rodeado de **tools y gates deterministas**, con el **humano en el cierre** — ni workflow, ni multiagente.

### Los 4 puntos a debatir (afirmación · porqué · qué descartamos)

**① ¿Por qué AGENTE y no workflow?**
- ✅ El orden de la conversación **no se puede predefinir**: cada cliente da los datos en distinto orden; el LLM decide en runtime qué preguntar y qué tool invocar.
- ❌ Descartamos workflow: cablear la secuencia mataría la conversación natural de WhatsApp.
- 🗣️ *Pregunta para el debate: ¿alguien ve una secuencia fija que yo no veo?*

**② ¿Por qué NO multiagente?**
- ✅ Un solo rol, un solo dominio, ~20 conversaciones/semana → agregar agentes suma costo y riesgo **sin fan-out real** ("no construyas agentes para todo").
- ❌ Descartamos multiagente hoy; queda la puerta abierta: el proveedor como **Agent-as-Tool** a futuro, sin cambiar la arquitectura.
- 🗣️ *Pregunta: ¿algún escenario real del negocio que exija un segundo agente YA?*

**③ ¿Dónde viven los pasos que SÍ conocemos?**
- ✅ En **código, no en el prompt**: gates deterministas (cobertura, factibilidad 72h/feriados, precio SOLO del motor de reglas zona×temporada + S/50, frase "referencial" obligatoria).
- ❌ Descartamos el paso a paso en el system prompt (el "workflow oculto" que Boris penaliza).

**④ ¿Dónde termina el agente?**
- ✅ En la **cotización**: la única escritura del agente es **insertar una cotización** en la BD (NO bloquea disponibilidad). El ciclo lo cierra el humano en la misma BD: el asesor la convierte en **reserva pendiente** (sigue sin bloquear) y, recibido el pago, en **reserva CONFIRMADA** (la única que bloquea disponibilidad). El agente jamás cobra ni reserva.
- 🗣️ *Pregunta: ¿estamos todos de acuerdo con ese límite? (Fernando: ¿así funciona hoy?)*

**Stack (para contexto del debate):** 🐳 Docker Compose local · BFF ⚡FastAPI + guardrails (y API externa si se necesita) · 🦜 `create_agent` · Chroma ← **PDFs del negocio** (políticas/condiciones/catálogo comercial) · 🐘 **PostgreSQL — la BD que la empresa ya usa para gestionar reservas** (catálogo, precios zona×temporada, calendario, cotizaciones→reservas, expedientes+preferencias y checkpointer) · LangSmith.

### ✍️ Borrador de síntesis para Classroom (pulir DESPUÉS del debate)

> El nuestro es un **agente único** (Goal-Based, patrón ReAct) porque el orden de la conversación lo decide el LLM en runtime según los datos que dé el cliente por WhatsApp. **No es workflow**: los pasos conocidos no van en el prompt, viven como gates deterministas en código (cobertura, factibilidad, precio solo del motor de reglas). **No es multiagente**: un solo rol y dominio con ~20 conversaciones/semana — más agentes sumarían costo sin beneficio; el proveedor podría integrarse a futuro como Agent-as-Tool. El cierre es **humano**: la única escritura del agente es **insertar la cotización** en el PostgreSQL que la empresa ya usa para gestionar reservas (no bloquea disponibilidad); el asesor la convierte en reserva pendiente y, con el pago, en **reserva confirmada — la única que bloquea disponibilidad**. Corre 100% dockerizado en local (FastAPI + LangChain `create_agent` + Chroma alimentado con los PDFs del negocio + ese **PostgreSQL como fuente de verdad**) con observabilidad en LangSmith. **Cumple el checklist de la S15** (¿compleja? ¿valiosa? ¿lograble? ¿costo del error?): la conversación es impredecible, es un negocio real (~20 cotizaciones/semana), el scope está acotado a cotizar, y el costo del error se controla con gates deterministas + cierre humano. **Adjuntamos además nuestro System Prompt (Goal-Based)** como evidencia de que no hay workflow oculto en el prompt.

## 2 · La arquitectura, capa por capa (cada caja existe por una razón)

| Capa / caja del diagrama | Qué hace | Por qué así (trade-off) |
|---|---|---|
| **Cliente WhatsApp → Meta Cloud API → webhook** | El canal REAL del negocio (~20 conv/sem) | El diseño postpone Twilio/otros BSP: la Cloud API de Meta es directa y barata a este volumen |
| **Consola Streamlit (demo)** | Pruebas internas y presentación en vivo del curso | No es el canal productivo; evita depender de WhatsApp para demos |
| **BFF ⚡FastAPI** | Sesiones, webhook, **guardrails de entrada/salida** (scope, injection, PII), rate limit; además **expone API REST externa** si otro sistema necesita consumir al agente a futuro | El agente nunca se expone directo (patrón de la clase S14); los guardrails viven en software, no en el prompt; FastAPI ya nos da la puerta de integración sin refactor |
| **Agente `create_agent` (LangChain v1)** | Goal-Based + ReAct; System Prompt versionado como secreto | Harness listo del curso; un solo agente = mínima autonomía |
| **Checkpointer (PostgresSaver)** | Memoria de corto plazo por `thread_id` (trim + summary por umbral de tokens) | Reusa el mismo PostgreSQL de la plataforma: una sola pieza de persistencia que operar |
| **Tools deterministas** (`consulta_catalogo`, `validar_cobertura`, `validar_disponibilidad`, `calcular_cotizacion`, `motor_comparacion`, `preferencias`, `registrar_cotizacion`, `derivar_a_asesor`) | Todo dato duro sale de aquí; el **motor de comparación** rankea alternativas con pesos definidos por el negocio (el LLM explica el resultado, no puede cambiar los pesos); `preferencias` solo guarda con consentimiento explícito | **El precio jamás lo genera el LLM**: base por zona×temporada + adicionales (S/50 sin ascensor) = motor de reglas |
| **PostgreSQL — la BD que la empresa YA USA para gestionar reservas** (catálogo, precios, calendario, cotizaciones→reservas, expedientes+preferencias) | La única escritura del agente es `registrar_cotizacion` (**insert que NO bloquea disponibilidad**). El ciclo vive en la misma BD: cotización → reserva **pendiente** (asesor, sin bloquear) → pago → reserva **CONFIRMADA** (asesor, bloquea) | Nos conectamos al sistema real del negocio en vez de inventar otro almacén (una sola fuente de verdad); **transacciones ACID** para el control de doble-booking; la misma base guarda datos + memoria (menos piezas que operar) |
| **Chroma (RAG) ← PDFs del negocio** | El conocimiento no estructurado (políticas, condiciones, catálogo comercial descriptivo) se ingesta desde los **PDFs reales** vía embeddings; el agente lo consulta como **Agentic RAG** (retrieval = tool) | Conocimiento no estructurado (PDFs) separado del dato duro estructurado (tablas) — regla de la S13; cada fuente del card §3.1 tiene su almacén |
| **Asesor humano (WhatsApp)** | Recibe el expediente por WhatsApp (sin CRM: así opera hoy el negocio); convierte cotización → reserva pendiente → **confirmada tras el pago** — es el único que bloquea disponibilidad | El pago y el compromiso de stock son irreversibles → HITL siempre (y Ley 31601: derecho a humano) |
| **LangSmith** | Trazas por thread/turn, tokens/costos, evaluadores | Observabilidad de la clase S12/S14; base de los KPIs del card §6 |
| **🐳 Docker Compose (local)** | 4 contenedores: `bff-agente` (⚡FastAPI + 🦜LangChain) · `chroma` · `postgres` 🐘 · `demo` (📊Streamlit). `docker compose up` levanta TODO en local | A 20 conv/semana la nube no se justifica (Boris: "no es necesario que paguen nube"); portar después es `docker push`. Lo NO dockerizado es lo externo: WhatsApp API, OpenAI, LangSmith |
| **Canal de público abierto (SIN autenticación)** | Cualquier persona que escriba al WhatsApp del negocio es atendida; el número del cliente solo identifica la sesión (`thread_id`) | Es un canal comercial abierto: no aplica SSO/registro; los datos personales se piden recién en el cierre (minimización por etapa) |
| **Omisiones conscientes: WAF / AI Gateway / balanceo de LLM** | Perímetro = verificación de firma del webhook de Meta; una sola ruta al LLM | Con un promedio de **~20 conversaciones/semana** no se justifican; el BFF centraliza la llamada al LLM y permite añadirlos sin refactor si el volumen crece |

## 3 · Coherencia sustento ↔ diagrama (checklist antes de subir)

- [ ] El sustento dice **UN agente** → el diagrama tiene **UNA sola caja de agente** ✓
- [ ] El sustento dice "gates deterministas" → se ven como **tools/guardrails en el BFF**, no como pasos en el prompt ✓
- [ ] El sustento dice WhatsApp → el canal del diagrama es WhatsApp (no un chat genérico) ✓
- [ ] El precio "solo desde el motor de reglas" → hay flecha **tools → PostgreSQL**, ninguna del LLM a precios ✓
- [ ] La única escritura del agente es **insertar la cotización (NO bloquea disponibilidad)**; pendiente y confirmada son del asesor ✓
- [ ] HITL visible: **asesor humano + link de pago fuera del agente** ✓
- [ ] Nada de multiagente dibujado (Agent-as-Tool solo mencionado como futuro, no como caja) ✓

## 4 · Operativa de entrega

- **Editar el diagrama:** bajar `arquitectura-tus-eventos.drawio` (esta carpeta) → abrir en https://app.diagrams.net (o VS Code + extensión Draw.io) → ajustar → re-exportar el PNG (File → Export as → PNG) → re-subir ambos.
- **Subir a Classroom (responsable: definir en la reu):** pegar el texto del §1 en la caja + adjuntar `arquitectura-tus-eventos.png` (o el `.drawio`) **+ el System Prompt** (versión final limpia al pie de `profile-card/agentic-profile-card-grupo5-v3.md`) — Boris: *"si me agregan un System Prompt sería un plus"*.
- **Deadline interno del grupo: MIÉ 6-AGO por la noche** (un día de colchón).
- Fuentes de datos del negocio: respuestas de Fernando (5-ago) — canal, precios por zona/temporada, recargo S/50, calendario Excel, 72 h/feriados, datos de cierre y link de pago.
