Agentic Profile Card

Agente de ocasiones de consumo y eventos

Versión 1.0 · Tipo: Utility-Based Agent con memoria basada en modelo · Arquitectura monoagente

⸻

Communication Layer

Conversacional + no conversacional

El agente interactúa principalmente mediante WhatsApp, donde atiende consultas, identifica necesidades, recomienda alternativas y acompaña al consumidor hasta una cotización o derivación comercial.

También puede actuar de manera no conversacional mediante recordatorios autorizados. Estos recordatorios pueden activarse por fechas personales, como cumpleaños, o por momentos estacionales de consumo, como Navidad, Año Nuevo o celebraciones nacionales.

⸻

Context Definition

Domain Definition

El agente opera dentro de una empresa que comercializa productos y servicios para reuniones, celebraciones y eventos.

Su dominio no se limita a responder preguntas sobre un catálogo. También debe comprender la ocasión que está organizando el consumidor y relacionarla con una alternativa adecuada.

Por ejemplo, una reunión pequeña, una celebración familiar o un evento corporativo pueden necesitar recomendaciones diferentes. Para hacerlo, el agente considera información como el tipo de ocasión, la cantidad de asistentes, la fecha, el lugar y las preferencias del consumidor.

Objectives Definition

El objetivo principal es ayudar al consumidor a elegir una alternativa adecuada para su ocasión y facilitar su avance hacia una cotización o atención comercial.

Durante la conversación, el agente busca comprender la intención, recopilar solamente los datos que faltan y recomendar una categoría de producto o servicio. Cuando las reglas del caso están definidas, puede calcular una cotización simple. Cuando existe una excepción, negociación o condición especial, deriva la conversación a un asesor humano.

Además, puede mantener la relación con el consumidor mediante preferencias y fechas importantes que hayan sido autorizadas.

⸻

Environment Definition

Knowledge

El conocimiento del agente se encuentra en fuentes actualizadas y separadas de su memoria.

La base de conocimiento contiene información general sobre las categorías de productos y servicios, sus características, las ocasiones para las que pueden ser recomendados, preguntas frecuentes, cobertura y condiciones de atención.

El catálogo y las fuentes estructuradas contienen información que puede cambiar con mayor frecuencia, como precios, disponibilidad, formatos y reglas de cotización.

El agente también consulta un calendario comercial para reconocer temporadas o fechas relevantes. De esta manera, no depende solamente de lo que el modelo recuerde, sino de información vigente proporcionada por el negocio.

Tools

El agente utiliza herramientas para realizar acciones que no deberían depender únicamente del modelo de lenguaje.

Puede consultar el catálogo, validar cobertura y disponibilidad, aplicar reglas de factibilidad y calcular cotizaciones. También puede registrar una oportunidad comercial, consultar o actualizar preferencias autorizadas y transferir una conversación a un asesor.

Para los recordatorios, utiliza una herramienta que consulta fechas y consentimientos. La herramienta detecta que se aproxima una fecha, mientras que el agente decide cómo formular una comunicación relevante.

Short-Term Memory

La memoria de corto plazo conserva el estado de la conversación actual.

Incluye la intención del consumidor, la ocasión de consumo, la fecha, el lugar, la cantidad de asistentes, las preferencias mencionadas y las alternativas que ya fueron evaluadas.

También registra qué información falta y en qué etapa se encuentra la conversación. Esto permite que el agente no repita preguntas y que pueda continuar una cotización aunque la información haya sido entregada en diferentes mensajes.

Por ejemplo, si el consumidor ya mencionó que organiza un cumpleaños para veinte personas, el agente conserva esos datos y pregunta únicamente por la fecha, el lugar o las preferencias que todavía necesita.

Long-Term Memory

La memoria de largo plazo conserva información útil entre diferentes conversaciones.

Puede incluir preferencias confirmadas, categorías de interés, cotizaciones anteriores, ocasiones frecuentes y fechas importantes. También debe registrar si el consumidor autorizó recibir comunicaciones y cuándo fue enviado el último recordatorio.

Esta memoria permite que el agente reconozca a un consumidor recurrente y ofrezca una experiencia más personalizada. Sin embargo, las preferencias no deben inferirse automáticamente. Antes de guardarlas, el agente debe confirmarlas con el consumidor.

Los precios, la disponibilidad y las condiciones comerciales no se guardan en esta memoria, porque deben consultarse nuevamente desde las fuentes vigentes.

⸻

Autonomy Dimension Definition

Semiautónomo y restringido

El agente tiene autonomía para comprender solicitudes, responder consultas, recomendar alternativas, recopilar datos y realizar cotizaciones simples.

También puede guardar preferencias confirmadas y enviar recordatorios cuando existe consentimiento y se cumplen las reglas de frecuencia y horario.

Su autonomía termina cuando el caso requiere negociación o una decisión humana. No puede procesar pagos, aprobar descuentos, confirmar excepciones operativas ni resolver reclamos complejos.

La derivación no debe ser una transferencia sin contexto. El agente prepara un resumen con la necesidad del consumidor, los datos recopilados, la recomendación realizada, la cotización disponible y el motivo por el que se necesita intervención humana.

⸻

Criticality Dimension Definition

Nivel medio y controlado

El agente participa en decisiones comerciales y utiliza información personal, por lo que existen riesgos que deben ser controlados.

Uno de los principales riesgos es realizar una recomendación poco relevante por interpretar incorrectamente la ocasión o las preferencias del consumidor. También podría entregar una cotización incorrecta si utiliza información desactualizada.

En el uso de memoria de largo plazo, existe el riesgo de guardar datos que el consumidor no confirmó o de enviar recordatorios con demasiada frecuencia.

Para reducir estos riesgos, el agente debe consultar las fuentes vigentes antes de cotizar, confirmar las preferencias antes de almacenarlas y solicitar consentimiento para cualquier comunicación futura.

El consumidor debe poder corregir o eliminar sus datos y desactivar los recordatorios. Cuando el agente encuentre información incompleta, contradictoria o fuera de las reglas establecidas, debe derivar el caso en lugar de inventar una respuesta.

⸻

Objetivo general

Ayudar al consumidor a encontrar una alternativa adecuada para su ocasión, facilitar la cotización y mantener una relación relevante mediante preferencias y recordatorios autorizados.

Esta Profile Card corresponde a un sistema monoagente. El mismo agente mantiene la conversación y decide qué herramienta utilizar según la intención del consumidor. Aunque realiza diferentes funciones, todas comparten el mismo objetivo, contexto y memoria.
