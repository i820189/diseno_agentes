Agentic Profile Card

Agente de recomendaciones y atención para ocasiones de consumo

Versión: 1.0
Arquitectura: Monoagente
Tipo de agente: Goal-Based Agent con memoria basada en modelo
Nivel de autonomía: Semiautónomo y constreñido
Nivel de criticidad: Medio – controlado

⸻

1. Descripción general

El agente está pensado para atender consumidores que buscan productos o servicios para reuniones, celebraciones y eventos.

Su función principal es comprender la necesidad del usuario, identificar la ocasión de consumo, recomendar una alternativa adecuada y ayudarlo a avanzar hacia una cotización.

También puede conservar preferencias confirmadas y fechas importantes, como cumpleaños o aniversarios, para enviar recordatorios o recomendaciones futuras, siempre que exista consentimiento.

En este documento no se incluyen nombres del negocio, marcas, precios ni detalles específicos de productos.

⸻

2. Tipo de agente

El agente se clasifica principalmente como un:

Goal-Based Agent con memoria basada en modelo

Se considera un Goal-Based Agent porque sus decisiones están orientadas a alcanzar objetivos definidos:

* identificar la necesidad del consumidor;
* recomendar una alternativa;
* completar los datos necesarios;
* generar una cotización;
* derivar una oportunidad calificada a un asesor.

También incorpora características de un Model-Based Reflex Agent, porque mantiene un estado interno de la conversación y del consumidor. Este estado le permite recordar qué información ya fue entregada, qué datos faltan y en qué parte del proceso se encuentra.

En una versión futura podría incorporar una función de utilidad más desarrollada para comparar alternativas según precio, preferencia, cantidad de asistentes y disponibilidad. Sin embargo, para el alcance inicial se considera principalmente un agente basado en objetivos.

No se plantea como un Learning Agent autónomo, ya que no modifica sus reglas por sí solo.

⸻

3. Communication Layer

Conversacional

El usuario interactúa con el agente mediante lenguaje natural, principalmente a través de WhatsApp.

Puede realizar consultas como:

Estoy organizando un cumpleaños y necesito una opción para unas veinte personas.

Quiero conocer qué alternativas tienen para una reunión.

Necesito una cotización para una fecha determinada.

El agente debe comprender la solicitud, extraer los datos disponibles y preguntar únicamente por la información faltante.

No conversacional

El agente también puede participar en procesos automáticos como:

* consultar fechas importantes;
* detectar momentos estacionales;
* preparar recordatorios;
* revisar el estado de una cotización;
* registrar preferencias confirmadas;
* activar un seguimiento autorizado.

⸻

4. Context Definition

4.1 Domain Definition

Dominio: productos y servicios para ocasiones de consumo, reuniones y eventos.

El agente actúa como un asistente comercial que ayuda al consumidor a encontrar una alternativa según su necesidad.

Debe comprender conceptos como:

* tipo de ocasión;
* cantidad de asistentes;
* fecha;
* ubicación;
* preferencias;
* categorías de productos o servicios;
* condiciones de atención;
* restricciones operativas;
* cotización;
* seguimiento comercial.

El rol del system prompt será definir cómo debe comportarse el agente, qué información puede utilizar, qué decisiones puede tomar y cuándo debe derivar el caso a una persona.

4.2 Objectives Definition

Objetivo general

Ayudar al consumidor a elegir una alternativa adecuada para su ocasión y facilitar su avance hacia una cotización o atención humana.

Objetivos específicos

1. Comprender la intención del consumidor.
2. Identificar la ocasión de consumo.
3. Extraer los datos entregados durante la conversación.
4. Solicitar solamente la información faltante.
5. Recomendar una categoría de producto o servicio.
6. Consultar información actualizada.
7. Elaborar cotizaciones simples cuando sea posible.
8. Derivar casos complejos con un resumen.
9. Guardar preferencias únicamente con confirmación.
10. Enviar recordatorios cuando exista consentimiento.

⸻

5. Environment Definition

5.1 Knowledge

El conocimiento general del agente puede estar almacenado en una base de conocimiento consultada mediante RAG.

Esta base incluiría:

* descripción de las categorías ofrecidas;
* características de cada alternativa;
* ocasiones para las que pueden ser recomendadas;
* preguntas frecuentes;
* condiciones de atención;
* cobertura;
* restricciones operativas;
* políticas generales;
* mensajes comerciales aprobados.

Ground Truth

La información variable debe provenir de fuentes estructuradas y actualizadas, como:

* catálogo;
* tarifario;
* sistema de disponibilidad;
* lista de cobertura;
* reglas comerciales;
* calendario de fechas relevantes.

El agente no debe inventar precios, disponibilidad, características ni condiciones.

⸻

5.2 Tools

El agente puede utilizar las siguientes herramientas:

consultar_catalogo

Busca las categorías de productos o servicios disponibles.

consultar_alternativa

Obtiene información detallada de una opción.

validar_cobertura

Verifica si la ubicación se encuentra dentro de la zona de atención.

validar_factibilidad

Evalúa condiciones como fecha, anticipación y restricciones operativas.

calcular_cotizacion

Calcula una cotización cuando las reglas y datos están completos.

consultar_preferencias

Recupera preferencias autorizadas del consumidor.

guardar_preferencia

Registra una preferencia después de confirmarla.

consultar_fechas_importantes

Recupera fechas autorizadas, como cumpleaños o aniversarios.

programar_recordatorio

Registra un recordatorio para una fecha futura.

derivar_a_asesor

Transfiere el caso con los datos y el resumen de la conversación.

⸻

6. Memoria

6.1 Short-Term Memory

La memoria de corto plazo conserva el contexto de la conversación actual.

Puede incluir:

* intención;
* ocasión de consumo;
* fecha;
* ubicación;
* cantidad de asistentes;
* preferencias actuales;
* categoría recomendada;
* alternativas descartadas;
* datos faltantes;
* cotización en proceso;
* etapa de la conversación.

Ejemplo:

{
  "session_id": "SESION-001",
  "intencion": "solicitar_recomendacion",
  "ocasion": "cumpleaños",
  "asistentes": 20,
  "fecha": "pendiente",
  "preferencia_actual": "alternativa_practica",
  "estado": "recopilando_datos"
}

Esta memoria evita que el agente repita preguntas y permite mantener continuidad.

Por ejemplo, si el consumidor ya indicó que se trata de un cumpleaños para veinte personas, el agente no debería volver a solicitar esos datos.

⸻

6.2 Long-Term Memory

La memoria de largo plazo conserva información útil entre diferentes conversaciones.

Puede incluir:

* preferencias confirmadas;
* categorías de interés;
* tipos de eventos frecuentes;
* cotizaciones anteriores;
* compras anteriores autorizadas;
* cumpleaños o aniversarios;
* recordatorios enviados;
* consentimiento para comunicaciones;
* solicitudes de actualización o eliminación.

Ejemplo:

{
  "usuario_id": "USUARIO-001",
  "preferencias": {
    "tipo_de_ocasion": "reuniones_familiares",
    "alternativa_preferida": "solucion_practica"
  },
  "fecha_importante": {
    "tipo": "cumpleaños",
    "mes": "noviembre"
  },
  "consentimiento_recordatorios": true
}

La memoria de largo plazo no debe utilizarse como fuente de precios, stock o reglas, porque esa información puede cambiar.

⸻

7. Política de memoria

El agente debe distinguir entre información temporal y permanente.

Información temporal

Ejemplo:

Para este evento prefiero una opción sencilla.

Esta preferencia se utiliza únicamente en la conversación actual.

Información permanente

Ejemplo:

En mis reuniones siempre prefiero opciones sencillas.

Antes de guardarla, el agente debe consultar:

¿Deseas que recuerde esta preferencia para futuras recomendaciones?

Fechas importantes

Si el consumidor comparte su cumpleaños o aniversario, el agente debe explicar para qué desea almacenarlo.

Ejemplo:

¿Deseas que recuerde esta fecha para enviarte un recordatorio antes de tu próxima celebración?

El consumidor debe poder consultar, modificar o eliminar esta información.

⸻

8. Mecanismo de recomendación

El agente primero debe descartar las opciones que no cumplen condiciones obligatorias.

Luego puede evaluar alternativas considerando:

Criterio	Importancia inicial
Compatibilidad con la ocasión	Alta
Cantidad de asistentes	Alta
Preferencias del consumidor	Media
Presupuesto aproximado	Media
Disponibilidad	Alta
Facilidad operativa	Media

En esta primera versión no se propone una fórmula matemática compleja. El agente aplica reglas y criterios definidos por el negocio para recomendar una alternativa y explicar el motivo.

Ejemplo:

Esta opción podría ser adecuada porque se trata de una reunión pequeña, buscas algo práctico y no necesitas una solución con muchos equipos adicionales.

⸻

9. Autonomy Dimension Definition

Nivel de autonomía

Semiautónomo y constreñido

El agente puede:

* comprender la solicitud;
* recopilar información;
* consultar fuentes;
* recomendar alternativas;
* validar reglas simples;
* calcular cotizaciones básicas;
* guardar preferencias confirmadas;
* preparar recordatorios;
* derivar casos a un asesor.

El agente no puede:

* realizar y confirmar pagos;
* aprobar descuentos;
* negociar condiciones especiales;
* confirmar excepciones;
* modificar reglas comerciales;
* resolver reclamos complejos;
* almacenar preferencias sin autorización;
* enviar comunicaciones sin consentimiento.

Human-in-the-loop

El asesor humano participa cuando:

* el consumidor quiere cerrar la compra;
* existe negociación;
* se solicita una excepción;
* falta información operativa;
* existe un reclamo;
* el usuario solicita hablar con una persona;
* el agente no puede resolver el caso con seguridad.

⸻

10. Criticality Dimension Definition

Nivel de criticidad

Medio – controlado

El agente puede influir en una decisión de compra y utiliza información personal para personalizar la atención, pero no ejecuta pagos ni toma decisiones de alto impacto.

Riesgos principales

* recomendación poco relevante;
* interpretación incorrecta de la ocasión;
* cotización equivocada;
* uso de información desactualizada;
* preferencia guardada incorrectamente;
* envío excesivo de recordatorios;
* pérdida del contexto;
* exposición de información personal;
* derivación tardía al asesor.

⸻

11. Guardrails and Controls

1. No inventar precios, productos o condiciones.
2. Consultar las fuentes vigentes antes de cotizar.
3. Solicitar confirmación antes de guardar preferencias.
4. Solicitar consentimiento antes de enviar recordatorios.
5. No guardar toda la conversación como memoria permanente.
6. Permitir actualizar o eliminar información.
7. Limitar la frecuencia de mensajes.
8. Separar la información de cada consumidor.
9. Derivar los casos ambiguos o fuera de las reglas.
10. No procesar pagos ni almacenar información financiera sensible.

⸻

12. Evaluaciones

El agente podría evaluarse mediante:

Métrica	Descripción
Precisión de intención	Identifica correctamente lo que busca el usuario
Completitud del contexto	Conserva los datos entregados
Relevancia	La recomendación coincide con la ocasión
Exactitud factual	La información coincide con las fuentes
Calidad de cotización	Aplica correctamente las reglas
Corrección de memoria	Guarda solo información confirmada
Tasa de preguntas repetidas	Mide pérdida de contexto
Derivación útil	El asesor recibe información suficiente
Latencia	Tiempo de respuesta
Satisfacción	Evaluación del consumidor

⸻

13. LLM as a Judge

Un modelo evaluador podría revisar:

1. Si el agente comprendió la intención.
2. Si utilizó correctamente el contexto.
3. Si repitió preguntas ya respondidas.
4. Si la recomendación fue coherente.
5. Si inventó información.
6. Si diferenció memoria temporal y permanente.
7. Si solicitó consentimiento antes de guardar datos.
8. Si derivó correctamente los casos complejos.
9. Si la respuesta fue clara y breve.
10. Si el usuario mantuvo el control final.

⸻

14. Flujo funcional

Usuario inicia la conversación
        ↓
El agente identifica la intención y la ocasión
        ↓
Extrae la información disponible
        ↓
Actualiza la memoria de corto plazo
        ↓
Consulta preferencias autorizadas
        ↓
Identifica información faltante
        ↓
Realiza preguntas de aclaración
        ↓
Consulta catálogo, reglas y disponibilidad
        ↓
Recomienda una alternativa
        ↓
Calcula una cotización cuando es posible
        ↓
Deriva a un asesor o finaliza la consulta
        ↓
Solicita confirmación para guardar preferencias
        ↓
Actualiza memoria de largo plazo

⸻

15. Ejemplo de interacción

Usuario:

Estoy organizando un cumpleaños para unas veinte personas y necesito algo práctico.

Agente:

Para recomendarte una opción adecuada, ¿en qué fecha será y en qué zona se realizará?

Usuario:

Será el próximo mes. Normalmente prefiero opciones simples para mis reuniones.

Agente:

Tomaré en cuenta una alternativa práctica para esta ocasión. ¿Deseas que recuerde que normalmente prefieres opciones simples para futuras recomendaciones?

Usuario:

Sí.

Agente:

Listo. Guardaré esa preferencia. Ahora revisaré las alternativas disponibles para la fecha y zona indicadas.

⸻

16. Resumen ejecutivo

Dimensión	Definición
Communication Layer	Conversacional y no conversacional
Domain	Ocasiones de consumo, reuniones y eventos
Objetivo	Recomendar, cotizar y derivar oportunidades
Tipo de agente	Goal-Based Agent con memoria basada en modelo
Knowledge	Catálogo, reglas, cobertura y base de conocimiento
Tools	Consultar, validar, cotizar, recordar y derivar
Short-Term Memory	Contexto de la conversación actual
Long-Term Memory	Preferencias y fechas autorizadas
Autonomía	Semiautónomo y constreñido
Criticidad	Media – controlada
Control humano	Obligatorio para negociación, cierre y excepciones
Resultado esperado	Recomendación relevante y cotización más ágil
