# Tarea S14 — Arquitectura de Solución "Tus Eventos" (GRUPAL · 20 pts · due JUE 7-AGO 11:59pm)

> **Entrega en Classroom = 2 partes:** ① la **caja de texto** con el sustento (abajo, listo para pegar) · ② el **archivo** del diagrama (el `.drawio` de esta carpeta — Boris acepta el XML directo, o exportar PNG desde draw.io).
> **Criterio de Boris:** *"en base a eso [el sustento] debería yo ver LO MISMO en su arquitectura"* — por eso este doc mapea cada afirmación a una caja del diagrama.
> Basado en el **Profile Card v3.1** (`profile-card/agentic-profile-card-grupo5-v3.md`) y validado con los datos reales del negocio (Fernando).

---

## 1 · SUSTENTO — texto listo para pegar en Classroom

> **El nuestro es un AGENTE (único) debido a que** el orden de la conversación no se puede predefinir: cada cliente llega por WhatsApp con datos distintos y en distinto orden, y es el LLM quien decide en runtime qué preguntar, qué herramienta invocar (catálogo, cobertura, factibilidad, cotización) y cuándo derivar — el patrón ReAct con objetivo (Goal-Based): entregar una cotización referencial válida.
> **No es un workflow** porque no hay secuencia fija que podamos cablear en código sin perder la conversación natural (los pasos conocidos NO van en el prompt: viven como gates deterministas alrededor del agente — validación de cobertura, factibilidad, precio solo desde el motor de reglas, y frase "referencial" obligatoria).
> **No es un multiagente** porque hay un solo rol y un solo dominio (venta/cotización de equipos para eventos) y un volumen de ~20 conversaciones/semana: agregar agentes solo sumaría costo y riesgo sin fan-out real ("no construyas agentes para todo"). La colaboración existe pero es **humano-en-el-loop**: cotización aceptada → expediente → el asesor genera el link de pago; y a futuro el proveedor podría integrarse como Agent-as-Tool sin cambiar la arquitectura.
> La solución corre **en Docker local** (BFF FastAPI + agente LangChain `create_agent` + Chroma para FAQ/políticas + SQLite para memoria y catálogo sincronizado desde los Excel reales del negocio), con observabilidad en LangSmith.

## 2 · La arquitectura, capa por capa (cada caja existe por una razón)

| Capa / caja del diagrama | Qué hace | Por qué así (trade-off) |
|---|---|---|
| **Cliente WhatsApp → Meta Cloud API → webhook** | El canal REAL del negocio (~20 conv/sem) | El diseño postpone Twilio/otros BSP: la Cloud API de Meta es directa y barata a este volumen |
| **Consola Streamlit (demo)** | Pruebas internas y presentación en vivo del curso | No es el canal productivo; evita depender de WhatsApp para demos |
| **BFF FastAPI** | Sesiones, webhook, **guardrails de entrada/salida** (scope, injection, PII), rate limit | El agente nunca se expone directo (patrón de la clase S14); los guardrails viven en software, no en el prompt |
| **Agente `create_agent` (LangChain v1)** | Goal-Based + ReAct; System Prompt versionado como secreto | Harness listo del curso; un solo agente = mínima autonomía |
| **Checkpointer (SQLite)** | Memoria de corto plazo por `thread_id` (estrategia trim) | Suficiente a este volumen; migrable a Redis/Postgres sin tocar el agente |
| **Tools deterministas** (`consulta_catalogo`, `validar_cobertura`, `validar_factibilidad`, `calcular_cotizacion`, `derivar_a_asesor`) | Todo dato duro sale de aquí | **El precio jamás lo genera el LLM**: base por zona×temporada + adicionales (S/50 sin ascensor) = motor de reglas |
| **Catálogo + Calendario (SQLite) ← Job de sync ← Excel del negocio** | Los Excel reales (precios por zona×temporada; disponibilidad/reservas) se sincronizan a tablas | Las tools no leen Excel en runtime (frágil); el sync respeta cómo trabaja hoy el negocio en vez de forzar un sistema nuevo |
| **Chroma (RAG)** | FAQ/políticas/condiciones (docs en `conocimiento/`) como **Agentic RAG** (retrieval = tool) | Conocimiento no estructurado separado del dato duro estructurado — regla de la S13 |
| **DB clientes/expedientes** | Slots de cierre (solo tras aceptar) + preferencias con consentimiento | Minimización PII por etapa (Profile Card §6) |
| **Asesor humano (WhatsApp)** | Recibe el expediente; **genera el link de pago** y confirma la reserva definitiva | El pago y el compromiso de stock son irreversibles → HITL siempre (y Ley 31601: derecho a humano) |
| **LangSmith** | Trazas por thread/turn, tokens/costos, evaluadores | Observabilidad de la clase S12/S14; base de los KPIs del card §6 |
| **Docker Compose (local)** | bff+agente · chroma · db | A 20 conv/semana la nube no se justifica (Boris: "no es necesario que paguen nube"); portar después es `docker push` |

## 3 · Coherencia sustento ↔ diagrama (checklist antes de subir)

- [ ] El sustento dice **UN agente** → el diagrama tiene **UNA sola caja de agente** ✓
- [ ] El sustento dice "gates deterministas" → se ven como **tools/guardrails en el BFF**, no como pasos en el prompt ✓
- [ ] El sustento dice WhatsApp → el canal del diagrama es WhatsApp (no un chat genérico) ✓
- [ ] El precio "solo desde el motor de reglas" → hay flecha **tools → catálogo sincronizado**, ninguna del LLM a precios ✓
- [ ] HITL visible: **asesor humano + link de pago fuera del agente** ✓
- [ ] Nada de multiagente dibujado (Agent-as-Tool solo mencionado como futuro, no como caja) ✓

## 4 · Operativa de entrega

- **Editar el diagrama:** bajar `tareas/sesion-14-arquitectura-tus-eventos.drawio` → abrir en https://app.diagrams.net (o VS Code + extensión Draw.io) → ajustar → re-subir al repo.
- **Subir a Classroom (responsable: definir en la reu):** pegar el texto del §1 en la caja + adjuntar el `.drawio` (o exportar PNG: File → Export as → PNG).
- **Deadline interno del grupo: MIÉ 6-AGO por la noche** (un día de colchón).
- Fuentes de datos del negocio: respuestas de Fernando (5-ago) — canal, precios por zona/temporada, recargo S/50, calendario Excel, 72 h/feriados, datos de cierre y link de pago.
