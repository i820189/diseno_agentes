# Sustento de Arquitectura — "Tus Eventos" (Entrega S14)

> Acompaña al **diagrama final del equipo** (Azure/AKS, ago-2026) y se basa en el **Agentic Profile Card v3.2**.
> Criterio del profesor: *"en base al sustento debería yo ver LO MISMO en su arquitectura"* — cada afirmación de abajo apunta a una caja del diagrama.

**La tesis en una línea:** **monoagente HÍBRIDO con flujo controlado** (la carátula del card): la **conversación la conduce el LLM** (ReAct) pero el **flujo lo controlan gates deterministas**; autonomía **semiautónoma y constreñida** (§4) — sus escrituras son acotadas (cotización, preferencia consentida, solicitud de derivación) y **ninguna bloquea disponibilidad**: el cierre es humano.

---

## Las 3 versiones del sustento — elegir en equipo

| Versión | Formato | Cuándo usarla |
|---|---|---|
| **V1 · Ejecutiva** | 1 párrafo (~150 palabras) | La **caja de texto de Classroom** |
| **V2 · Por capas** | Bullets con el porqué y lo descartado | El **Doc/PDF adjunto** (respaldo del diagrama) |
| **V3 · Defensa oral** | 6 preguntas y respuestas | Si Boris pregunta en vivo / revisión |

---

### V1 · Ejecutiva (pegar en Classroom)

> Nuestra solución es un **agente único, híbrido y con flujo controlado** — Goal-Based con patrón ReAct (`create_agent`, LangGraph debajo) — porque el orden de la conversación lo decide el LLM en runtime. **No es un workflow**: los pasos conocidos (datos mínimos, cobertura, disponibilidad, precio) viven como **gates deterministas en código**, no en el prompt. **No es multiagente**: un rol y un dominio con ~20 conversaciones/semana — más agentes sumarían costo sin fan-out real. Corre como **pods Python en AKS** detrás de **APIM**: API Service (FastAPI) para el webhook de WhatsApp, el monoagente y un **MCP Server** que expone las tools (catálogo, cobertura, disponibilidad, cotización por reglas, motor de comparación con pesos del negocio, preferencias con consentimiento y derivación). Los datos viven en **Cosmos DB** — transaccional (catálogo, reservas, cotizaciones, preferencias) y **vectorial para el RAG** (PDFs de políticas y cobertura, embebidos con `text-embedding-3-small`) — y **Redis** mantiene la memoria de sesión. **El agente solo INSERTA cotizaciones (no bloquea disponibilidad): el asesor humano las convierte en reserva pendiente y, tras el pago, en CONFIRMADA** — supervisión humana obligatoria (card §5.2) y derecho a humano (Ley 31601). Observabilidad con **LangSmith**; secretos y **system prompt versionado** en Key Vault.

### V2 · Por capas (para el Doc)

- **Canales + Exposición:** WhatsApp es el canal real del negocio (~20 conv/sem); **APIM** da claves, cuotas y WAF. *Evolución declarada:* el mismo APIM como **AI Gateway** (token limits = guardrail económico, semantic caching — doc compartida por el profesor en S14). *Descartado:* front propio con auth — es un canal comercial de público abierto; los datos personales se piden recién al cierre (minimización por etapa, card §5.2).
- **Aplicación (AKS):** pods Python con la **misma imagen** que corre en local — los manifests portan a AKS/EKS/GKE (*"te casas con esa nube"*, S14 → mitigado). **Monoagente**, no "orchestrator": el card define un solo rol. **MCP Server** desacopla las tools con un estándar abierto y gobernanza por **allowlist** (S11: MCPs envenenados); si conviene in-process, el cambio es mínimo (mismas tools).
- **Datos (Cosmos + Redis):** Cosmos guarda catálogo (incluye precios zona×temporada), reservas, cotizaciones y preferencias — **una sola fuente de verdad**. Los "sistemas oficiales" del card §3.2 **se materializan hoy en Cosmos**: el negocio no expone APIs, Cosmos ES el sistema oficial. Ahí vive el ciclo operativo validado con el negocio: **cotización → reserva PENDIENTE → pago → CONFIRMADA (bloquea)** — el asesor es **el único que bloquea disponibilidad**. Las restricciones operativas (72 h de anticipación, feriados) son **reglas en código** dentro de `validar_disponibilidad`, no interpretación del LLM. Redis = memoria de corto plazo (checkpointer por `thread_id`, S9). *Descartado:* una BD por componente — más piezas sin beneficio.
- **RAG:** Blob (PDFs del negocio) → **LangChain: ingesta + chunking + metadata** → `text-embedding-3-small` → **Cosmos vectorial** → **retriever como tool** (S13). El **mismo modelo** embebe ingesta y consulta (*"te casas con tu embedding model"*, S13). La **cobertura se extrae a zonas estructuradas en la ingesta**: la FAQ se responde por búsqueda semántica, pero el gate de cobertura compara contra lista (determinista). *Descartado:* Azure AI Search — el profesor validó Cosmos como vector DB en S13 ("se puede hacer vector database con Cosmos"); una familia de datos = menos piezas y costo.
- **LLM Provider:** `gpt-4o-mini` (razonamiento) + `text-embedding-3-small` (RAG) — **dos deployments del mismo recurso**; en despliegue enterprise se consumen vía **Azure OpenAI** para que la conversación del cliente no salga del tenant (Private Link + identidad administrada).
- **Seguimientos no conversacionales (card §1):** un **CronJob en AKS** dispara los recordatorios autorizados (vigencia de la cotización, solicitudes pendientes) por la misma API de WhatsApp — mismo perímetro, sin mantener al agente despierto.
- **Transversal:** Key Vault (secretos + **system prompt como secreto versionado**, S12) · LangSmith (trazas, tokens, evals) · guardrails E/S en software — incluida la **inyección vía documentos recuperados** (card §5.2) — · **reintentos limitados (5) con derivación por exceso** · el usuario puede **consultar o eliminar sus preferencias** (tool `preferencias`) · **evals con reglas determinísticas** (intención, extracción, faltantes, precios nunca inventados, derivación exacta).
- **Checklist S15:** ✔ conversación impredecible (agente, no workflow) · ✔ negocio real (~20 cotizaciones/sem) · ✔ scope acotado (recomendar-cotizar-derivar) · ✔ costo del error controlado (gates deterministas + cierre humano).

### V3 · Defensa oral (Q&A)

1. **¿Por qué agente y no workflow?** El orden lo decide el LLM en runtime según lo que dé el cliente; lo predecible vive como gates en código — un workflow cablearía la conversación y un prompt-con-pasos sería un "workflow oculto".
2. **¿Por qué no multiagente?** Un rol, un dominio, ~20 conv/semana: no hay fan-out que justifique el costo. El MCP Server deja la puerta abierta: un segundo agente consumiría las mismas tools sin duplicar lógica.
3. **¿Por qué MCP Server?** *(nuestra pregunta abierta al profesor)* Desacople con estándar abierto + gobernanza por allowlist (S11). Trade-off asumido: un hop más de latencia a cambio de tools reusables y auditables. Si recomienda in-process, migrar es trivial.
4. **¿Por qué Cosmos como vector DB y no AI Search?** Lo dijo el profesor en S13: "se puede hacer vector database con Cosmos". Una familia de datos para lo transaccional y lo vectorial = menos servicios, menos costo, un solo plano de gobierno.
5. **¿Dónde termina la autonomía del agente?** En el insert de la cotización — **no bloquea disponibilidad, no cobra, no confirma** (card §4). El asesor convierte pendiente → confirmada tras el pago y recibe el expediente completo de derivación (resumen, datos, validaciones, alternativa, motivo — card §3.2).
6. **¿Cómo llegan al LLM?** Con identidad administrada y endpoint privado; al crecer, el APIM existente asume el rol de **AI Gateway** (token rate limiting como control de presupuesto, caching semántico, métricas por app — S14).

---

## Mapeo Card v3.2 → diagrama (trazabilidad)

| Card | Caja del diagrama |
|---|---|
| §1 Conversacional (WhatsApp/Web) | Canales → APIM → API Service |
| §2.2 Recomendación · Cotización · Derivación | Monoagente + MCP tools + Atención humana/Derivación |
| §3.1 Catálogo / disponibilidad / restricciones | Cosmos (catálogo, reservas) + PDFs → RAG |
| §3.2 Las 7 conexiones (tools) | MCPServer–Tools (catálogo, cobertura, disponibilidad, precios, comparación, preferencias, atención humana) |
| §3.3 / §3.4 Memoria corto / largo plazo | Redis (sesión) / Cosmos (preferencias con consentimiento, cotizaciones) |
| §4 "No puede" (pagos, cerrar venta, inventar) | Gates en tools + ciclo: solo el asesor CONFIRMA |
| §5.1 Riesgos (precio incorrecto, doble-booking, PII) | Control de precios por reglas · única fuente de verdad · aislamiento por sesión |
| §5.2 Guardrails y Evals | Guardrails E/S (software) + evals deterministas + LangSmith |

## Notas para quien expone (los 3 flancos débiles y su respuesta)

1. **"Veo dos Cosmos distintos (NoSQL y MongoDB vCore)"** → "Misma familia; y tenemos identificada la unificación a **Cosmos NoSQL con índice DiskANN** para que transaccional y vectorial vivan en la misma cuenta — está en el backlog."
2. **"¿OpenAI directo? ¿Y el compliance?"** → "Mismos modelos vía **Azure OpenAI** en despliegue productivo: el dato no sale del tenant; el logo del diagrama refiere al modelo, el consumo es por el recurso Azure."
3. **"¿Y el asesor humano dónde está?"** → señalar la tarjeta **Atención humana / Derivación** + este sustento: la derivación incluye el expediente completo y el asesor es el único que convierte y bloquea. (Recomendación interna: darle una caja más visible en la próxima iteración del diagrama.)
4. **"Su card dice criticidad Media-Alta en la carátula y Media en §5"** → reconocerlo: "discrepancia interna del card detectada; el nivel operativo es **Media-Alta controlada** por tratarse de decisión comercial + PII — lo corregimos en la próxima versión del card."
