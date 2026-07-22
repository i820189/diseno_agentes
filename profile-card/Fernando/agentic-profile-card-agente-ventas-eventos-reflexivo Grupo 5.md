# Agentic Profile Card

## Agente de recomendaciones y atención para ocasiones de consumo

**Versión:** 2.0  
**Arquitectura:** Monoagente híbrido  
**Tipo de agente:** Model-Based Reflex Agent con componentes Goal-Based, Simple Reflex y Utility-Based básico  
**Integración principal:** Large Language Model (LLM)  
**Nivel de autonomía:** Semiautónomo y constreñido  
**Nivel de criticidad:** Medio – controlado

---

## 1. Descripción general

El agente está pensado para atender consumidores que buscan productos o servicios para reuniones, celebraciones y eventos.

Su función principal es comprender la necesidad del usuario, identificar la ocasión de consumo, recopilar la información necesaria, recomendar una alternativa adecuada y ayudarlo a avanzar hacia una cotización.

Para desarrollar este comportamiento se propone utilizar una combinación de modelos de agentes reflexivos. El **Model-Based Reflex Agent** será la arquitectura principal porque permitirá mantener un estado interno de la conversación. También se incorporarán componentes de un **Goal-Based Agent** para orientar las acciones hacia un resultado, reglas de un **Simple Reflex Agent** para validaciones directas y una aplicación básica de un **Utility-Based Agent** para comparar alternativas.

El agente estará integrado con un **LLM**, que será utilizado para comprender los mensajes del usuario, extraer información, identificar intenciones, generar respuestas y elaborar resúmenes. Sin embargo, las validaciones críticas y la información comercial deberán depender de reglas y fuentes estructuradas.

El agente también puede conservar preferencias confirmadas y fechas importantes, como cumpleaños o aniversarios, para enviar recordatorios o recomendaciones futuras, siempre que exista consentimiento.

En este documento no se incluyen nombres del negocio, marcas, precios ni detalles específicos de productos.

---

## 2. Tipo de agente

El agente se clasifica como un agente híbrido que combina cuatro modelos reflexivos.

### 2.1 Model-Based Reflex Agent

El **Model-Based Reflex Agent** será la arquitectura principal.

Este modelo permitirá que el agente mantenga un estado interno de la conversación y pueda recordar:

- qué información ya fue entregada;
- qué datos todavía faltan;
- qué alternativas fueron revisadas;
- qué opciones fueron descartadas;
- en qué etapa del proceso se encuentra el consumidor;
- cuál debería ser la siguiente acción.

Por ejemplo, si el usuario primero indica que está organizando un cumpleaños para veinte personas y luego señala la fecha y ubicación, el agente deberá unir estos datos dentro de un mismo estado.

Ejemplo de estado interno:

```json
{
  "intencion": "solicitar_cotizacion",
  "ocasion": "cumpleaños",
  "asistentes": 20,
  "fecha": "15-08-2026",
  "ubicacion": "Miraflores",
  "presupuesto": "no_informado",
  "estado_conversacion": "validando_factibilidad"
}
```

Este modelo es importante porque el agente no debería reaccionar solamente al último mensaje recibido. También debe considerar el contexto acumulado durante la conversación.

### 2.2 Goal-Based Agent

El agente también tendrá características de un **Goal-Based Agent**, porque sus decisiones estarán orientadas a alcanzar objetivos específicos.

El objetivo general será ayudar al consumidor a elegir una alternativa adecuada y avanzar hacia una cotización o atención humana.

Para lograrlo, el agente tendrá metas intermedias:

1. identificar la intención;
2. comprender la ocasión de consumo;
3. completar los datos mínimos;
4. validar cobertura y factibilidad;
5. recomendar una alternativa;
6. generar una cotización básica;
7. derivar el caso cuando corresponda.

El agente utilizará el estado interno para decidir qué acción lo acerca más al objetivo.

Por ejemplo, si ya conoce la ocasión y la cantidad de asistentes, pero todavía no conoce la fecha, su siguiente acción será solicitar ese dato en lugar de realizar una recomendación incompleta.

### 2.3 Simple Reflex Agent

El agente incluirá reglas de tipo **Simple Reflex Agent** para aplicar validaciones puntuales mediante condiciones directas.

Estas reglas seguirán una lógica básica:

```text
SI ocurre una condición
ENTONCES ejecutar una acción
```

Ejemplos:

```text
SI el usuario solicita hablar con una persona
ENTONCES derivar a un asesor.
```

```text
SI faltan datos obligatorios
ENTONCES preguntar únicamente por los datos faltantes.
```

```text
SI la ubicación está fuera de cobertura
ENTONCES informar la restricción y no generar una cotización automática.
```

```text
SI el usuario solicita un descuento o una excepción
ENTONCES derivar el caso a un asesor.
```

Estas reglas serán útiles para controlar decisiones que no deberían depender solamente de la interpretación del LLM.

### 2.4 Utility-Based Agent básico

El agente también incorporará un uso inicial y sencillo de un **Utility-Based Agent**.

Este componente permitirá comparar alternativas que ya hayan superado las condiciones obligatorias. La utilidad no se calculará mediante una fórmula avanzada, sino mediante una puntuación básica basada en criterios definidos.

Los criterios podrían incluir:

- compatibilidad con la ocasión;
- capacidad para la cantidad de asistentes;
- disponibilidad;
- preferencias del consumidor;
- presupuesto aproximado;
- facilidad operativa.

La alternativa con mayor puntuación podrá ser recomendada, siempre que cumpla las reglas obligatorias.

Este componente no busca optimizar todas las decisiones posibles. Se plantea como una primera aproximación académica para entender cómo un agente puede comparar opciones y seleccionar la más conveniente.

### 2.5 Modelo no incluido

No se plantea como un **Learning Agent** autónomo, ya que el agente no modificará sus reglas, criterios o comportamiento por sí solo.

Las mejoras se realizarán de manera supervisada mediante revisión de conversaciones, evaluación de resultados y actualización manual de prompts, reglas o fuentes de conocimiento.

---

## 3. Communication Layer

### Conversacional

El usuario interactúa con el agente mediante lenguaje natural, principalmente a través de WhatsApp.

Puede realizar consultas como:

> Estoy organizando un cumpleaños y necesito una opción para unas veinte personas.

> Quiero conocer qué alternativas tienen para una reunión.

> Necesito una cotización para una fecha determinada.

El LLM deberá comprender la solicitud, identificar la intención, extraer los datos disponibles y generar una respuesta natural.

Luego, el agente actualizará su estado interno y preguntará únicamente por la información faltante.

### No conversacional

El agente también puede participar en procesos automáticos como:

- consultar fechas importantes;
- detectar momentos estacionales;
- preparar recordatorios;
- revisar el estado de una cotización;
- registrar preferencias confirmadas;
- activar un seguimiento autorizado.

Estos procesos deberán respetar las reglas de consentimiento y frecuencia de contacto.

---

## 4. Context Definition

### 4.1 Domain Definition

**Dominio:** productos y servicios para ocasiones de consumo, reuniones y eventos.

El agente actúa como un asistente comercial que ayuda al consumidor a encontrar una alternativa según su necesidad.

Debe comprender conceptos como:

- tipo de ocasión;
- cantidad de asistentes;
- fecha;
- ubicación;
- preferencias;
- presupuesto aproximado;
- categorías de productos o servicios;
- condiciones de atención;
- restricciones operativas;
- cobertura;
- disponibilidad;
- cotización;
- seguimiento comercial.

El rol del system prompt será definir cómo debe comportarse el agente, qué información puede utilizar, qué decisiones puede tomar, cuáles son sus objetivos y cuándo debe derivar el caso a una persona.

### 4.2 Objectives Definition

#### Objetivo general

Ayudar al consumidor a elegir una alternativa adecuada para su ocasión y facilitar su avance hacia una cotización o atención humana.

#### Objetivos específicos

1. Comprender la intención del consumidor mediante el LLM.
2. Identificar la ocasión de consumo.
3. Extraer los datos entregados durante la conversación.
4. Actualizar el estado interno del agente.
5. Solicitar solamente la información faltante.
6. Validar condiciones obligatorias mediante reglas.
7. Consultar información actualizada.
8. Comparar alternativas disponibles.
9. Recomendar una categoría de producto o servicio.
10. Elaborar cotizaciones simples cuando sea posible.
11. Derivar casos complejos con un resumen.
12. Guardar preferencias únicamente con confirmación.
13. Enviar recordatorios cuando exista consentimiento.

### 4.3 Estados principales de la conversación

Para facilitar la implementación del Model-Based Reflex Agent, se proponen los siguientes estados:

1. `inicio`
2. `identificando_intencion`
3. `recopilando_datos`
4. `validando_condiciones`
5. `consultando_alternativas`
6. `evaluando_alternativas`
7. `presentando_recomendacion`
8. `generando_cotizacion`
9. `derivando_a_asesor`
10. `consulta_finalizada`

El estado podrá cambiar de acuerdo con la información recibida y las acciones ejecutadas.

---

## 5. Environment Definition

### 5.1 Knowledge

El conocimiento general del agente puede estar almacenado en una base de conocimiento consultada mediante RAG.

Esta base incluiría:

- descripción de las categorías ofrecidas;
- características de cada alternativa;
- ocasiones para las que pueden ser recomendadas;
- preguntas frecuentes;
- condiciones de atención;
- cobertura;
- restricciones operativas;
- políticas generales;
- mensajes comerciales aprobados.

El LLM puede utilizar esta información para comprender y explicar las alternativas, pero no debe asumir que toda la información recuperada está actualizada.

#### Ground Truth

La información variable debe provenir de fuentes estructuradas y actualizadas, como:

- catálogo;
- tarifario;
- sistema de disponibilidad;
- lista de cobertura;
- reglas comerciales;
- calendario de fechas relevantes.

El agente no debe inventar precios, disponibilidad, características ni condiciones.

### 5.2 Tools

El agente puede utilizar las siguientes herramientas:

#### `consultar_catalogo`

Busca las categorías de productos o servicios disponibles.

#### `consultar_alternativa`

Obtiene información detallada de una opción.

#### `validar_cobertura`

Verifica si la ubicación se encuentra dentro de la zona de atención.

#### `validar_factibilidad`

Evalúa condiciones como fecha, anticipación y restricciones operativas.

#### `consultar_disponibilidad`

Verifica si una alternativa se encuentra disponible para la fecha indicada.

#### `calcular_cotizacion`

Calcula una cotización cuando las reglas y datos están completos.

#### `evaluar_alternativas`

Asigna una puntuación básica a las opciones que cumplen las condiciones obligatorias.

#### `consultar_preferencias`

Recupera preferencias autorizadas del consumidor.

#### `guardar_preferencia`

Registra una preferencia después de confirmarla.

#### `consultar_fechas_importantes`

Recupera fechas autorizadas, como cumpleaños o aniversarios.

#### `programar_recordatorio`

Registra un recordatorio para una fecha futura.

#### `derivar_a_asesor`

Transfiere el caso con los datos y el resumen de la conversación.

### 5.3 Funciones del LLM

El LLM será utilizado para:

- comprender mensajes en lenguaje natural;
- identificar la intención del consumidor;
- extraer datos relevantes;
- detectar información ambigua;
- generar preguntas de aclaración;
- explicar una recomendación;
- redactar respuestas claras;
- elaborar un resumen para el asesor.

El LLM no será considerado la fuente de verdad para precios, stock, cobertura o disponibilidad.

---

## 6. Memoria

### 6.1 Short-Term Memory

La memoria de corto plazo conserva el contexto de la conversación actual y representa el estado interno del **Model-Based Reflex Agent**.

Puede incluir:

- intención;
- ocasión de consumo;
- fecha;
- ubicación;
- cantidad de asistentes;
- presupuesto aproximado;
- preferencias actuales;
- categoría recomendada;
- alternativas evaluadas;
- alternativas descartadas;
- datos faltantes;
- cotización en proceso;
- etapa de la conversación;
- última acción realizada;
- siguiente objetivo.

Ejemplo:

```json
{
  "session_id": "SESION-001",
  "intencion": "solicitar_recomendacion",
  "ocasion": "cumpleaños",
  "asistentes": 20,
  "fecha": "pendiente",
  "ubicacion": "Miraflores",
  "preferencia_actual": "alternativa_practica",
  "datos_faltantes": ["fecha"],
  "estado": "recopilando_datos",
  "siguiente_objetivo": "completar_datos_minimos"
}
```

Esta memoria evita que el agente repita preguntas y permite mantener continuidad.

Por ejemplo, si el consumidor ya indicó que se trata de un cumpleaños para veinte personas, el agente no debería volver a solicitar esos datos.

### 6.2 Actualización del estado interno

Después de cada mensaje, el agente deberá:

1. interpretar el mensaje mediante el LLM;
2. extraer la información nueva;
3. actualizar los datos conocidos;
4. conservar los datos anteriores que continúan siendo válidos;
5. identificar los datos faltantes;
6. actualizar el estado de la conversación;
7. definir la siguiente acción.

Ejemplo:

```text
Estado anterior:
- ocasión: cumpleaños
- asistentes: 20
- fecha: pendiente

Nuevo mensaje:
“Será el próximo sábado en Miraflores”.

Estado actualizado:
- ocasión: cumpleaños
- asistentes: 20
- fecha: próximo sábado
- ubicación: Miraflores
- estado: validando_condiciones
```

### 6.3 Long-Term Memory

La memoria de largo plazo conserva información útil entre diferentes conversaciones.

Puede incluir:

- preferencias confirmadas;
- categorías de interés;
- tipos de eventos frecuentes;
- cotizaciones anteriores;
- compras anteriores autorizadas;
- cumpleaños o aniversarios;
- recordatorios enviados;
- consentimiento para comunicaciones;
- solicitudes de actualización o eliminación.

Ejemplo:

```json
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
```

La memoria de largo plazo no debe utilizarse como fuente de precios, stock o reglas, porque esa información puede cambiar.

---

## 7. Política de memoria

El agente debe distinguir entre información temporal y permanente.

### Información temporal

Ejemplo:

> Para este evento prefiero una opción sencilla.

Esta preferencia se utiliza únicamente en la conversación actual.

### Información permanente

Ejemplo:

> En mis reuniones siempre prefiero opciones sencillas.

Antes de guardarla, el agente debe consultar:

> ¿Deseas que recuerde esta preferencia para futuras recomendaciones?

### Fechas importantes

Si el consumidor comparte su cumpleaños o aniversario, el agente debe explicar para qué desea almacenarlo.

Ejemplo:

> ¿Deseas que recuerde esta fecha para enviarte un recordatorio antes de tu próxima celebración?

El consumidor debe poder consultar, modificar o eliminar esta información.

El LLM puede ayudar a identificar que una preferencia podría ser permanente, pero el guardado solo debe ejecutarse después de una confirmación explícita.

---

## 8. Mecanismo de recomendación

El mecanismo de recomendación combinará reglas simples y una evaluación básica de utilidad.

### 8.1 Filtro mediante Simple Reflex Agent

El agente primero debe descartar las opciones que no cumplen condiciones obligatorias.

Ejemplos:

```text
SI una alternativa no tiene cobertura
ENTONCES descartarla.
```

```text
SI una alternativa no está disponible
ENTONCES descartarla.
```

```text
SI la cantidad de asistentes supera su capacidad
ENTONCES descartarla.
```

```text
SI no existe suficiente anticipación
ENTONCES derivar o informar la restricción.
```

### 8.2 Evaluación mediante Utility-Based Agent básico

Después de aplicar los filtros obligatorios, las alternativas restantes podrán evaluarse mediante una puntuación sencilla.

| Criterio | Peso inicial |
|---|---:|
| Compatibilidad con la ocasión | 30 % |
| Capacidad para asistentes | 20 % |
| Disponibilidad | 20 % |
| Preferencias del consumidor | 15 % |
| Presupuesto aproximado | 10 % |
| Facilidad operativa | 5 % |

Ejemplo de cálculo básico:

```text
Puntuación de utilidad =
compatibilidad + capacidad + disponibilidad + preferencias + presupuesto + facilidad
```

Cada criterio puede recibir un valor entre 0 y 100. Luego se aplica el peso correspondiente.

Ejemplo:

| Alternativa | Puntuación final |
|---|---:|
| Alternativa A | 88 |
| Alternativa B | 76 |
| Alternativa C | 64 |

El agente recomendará inicialmente la alternativa con mayor puntuación.

Esta fórmula es una primera versión y puede ajustarse después de realizar pruebas. No se busca construir todavía un modelo de optimización complejo.

### 8.3 Explicación mediante LLM

El LLM utilizará el resultado de las reglas y de la puntuación para generar una explicación natural.

Ejemplo:

> Esta opción podría ser adecuada porque tiene capacidad para veinte personas, se encuentra disponible para la fecha indicada y coincide con tu preferencia por una alternativa práctica.

El LLM no deberá modificar la puntuación calculada ni recomendar una opción que haya sido descartada por una regla obligatoria.

---

## 9. Autonomy Dimension Definition

### Nivel de autonomía

**Semiautónomo y constreñido**

El agente puede:

- comprender la solicitud mediante un LLM;
- extraer información;
- actualizar su estado interno;
- recopilar información faltante;
- consultar fuentes;
- aplicar reglas simples;
- comparar alternativas;
- recomendar opciones;
- validar condiciones básicas;
- calcular cotizaciones simples;
- guardar preferencias confirmadas;
- preparar recordatorios;
- derivar casos a un asesor.

El agente no puede:

- realizar y confirmar pagos;
- aprobar descuentos;
- negociar condiciones especiales;
- confirmar excepciones;
- modificar reglas comerciales;
- cambiar los pesos de utilidad por sí solo;
- resolver reclamos complejos;
- almacenar preferencias sin autorización;
- enviar comunicaciones sin consentimiento;
- aprender o modificar su comportamiento de forma autónoma.

### Human-in-the-loop

El asesor humano participa cuando:

- el consumidor quiere cerrar la compra;
- existe negociación;
- se solicita una excepción;
- falta información operativa;
- existe un reclamo;
- el usuario solicita hablar con una persona;
- el agente no puede resolver el caso con seguridad;
- dos alternativas presentan resultados similares y se requiere criterio comercial;
- existe una inconsistencia entre las fuentes consultadas.

---

## 10. Criticality Dimension Definition

### Nivel de criticidad

**Medio – controlado**

El agente puede influir en una decisión de compra y utiliza información personal para personalizar la atención, pero no ejecuta pagos ni toma decisiones de alto impacto.

### Riesgos principales

- recomendación poco relevante;
- interpretación incorrecta de la ocasión;
- pérdida o actualización incorrecta del estado interno;
- aplicación equivocada de una regla;
- puntuación de utilidad poco adecuada;
- cotización equivocada;
- uso de información desactualizada;
- preferencia guardada incorrectamente;
- envío excesivo de recordatorios;
- repetición de preguntas;
- exposición de información personal;
- derivación tardía al asesor;
- dependencia excesiva del LLM;
- generación de información no respaldada por herramientas.

---

## 11. Guardrails and Controls

1. No inventar precios, productos, disponibilidad o condiciones.
2. Consultar las fuentes vigentes antes de cotizar.
3. No permitir que el LLM modifique reglas obligatorias.
4. No permitir que el LLM recomiende opciones descartadas por cobertura, disponibilidad o capacidad.
5. Solicitar confirmación antes de guardar preferencias.
6. Solicitar consentimiento antes de enviar recordatorios.
7. No guardar toda la conversación como memoria permanente.
8. Permitir actualizar o eliminar información almacenada.
9. Limitar la frecuencia de mensajes.
10. Separar la información de cada consumidor.
11. Derivar los casos ambiguos o fuera de las reglas.
12. No procesar pagos ni almacenar información financiera sensible.
13. Mantener visibles los criterios utilizados para recomendar.
14. Registrar las herramientas y reglas aplicadas en cada decisión.
15. No cambiar automáticamente los pesos de utilidad.
16. Derivar si existe contradicción entre el estado interno y una fuente oficial.

---

## 12. Evaluaciones

El agente podría evaluarse mediante las siguientes métricas:

| Métrica | Descripción |
|---|---|
| Precisión de intención | Identifica correctamente lo que busca el usuario |
| Precisión de extracción | Recupera correctamente fecha, ubicación, ocasión y asistentes |
| Completitud del contexto | Conserva los datos entregados |
| Exactitud del estado interno | Actualiza correctamente la memoria de corto plazo |
| Tasa de preguntas repetidas | Mide pérdida de contexto |
| Cumplimiento de objetivos | Determina si la conversación avanza hacia una recomendación o cotización |
| Aplicación de reglas | Ejecuta correctamente las condiciones simples |
| Precisión de descarte | No recomienda alternativas que incumplen restricciones |
| Calidad de utilidad | Ordena las alternativas de acuerdo con los criterios definidos |
| Relevancia | La recomendación coincide con la ocasión |
| Exactitud factual | La información coincide con las fuentes |
| Calidad de cotización | Aplica correctamente las reglas de cálculo |
| Corrección de memoria | Guarda solo información confirmada |
| Derivación útil | El asesor recibe información suficiente |
| Latencia | Tiempo de respuesta |
| Satisfacción | Evaluación del consumidor |

### Evaluaciones por componente

#### Model-Based Reflex Agent

- conservación del contexto;
- actualización correcta del estado;
- identificación de datos faltantes;
- selección de la siguiente etapa.

#### Goal-Based Agent

- avance hacia el objetivo;
- cantidad de interacciones necesarias;
- finalización correcta del proceso;
- prevención de conversaciones sin dirección.

#### Simple Reflex Agent

- cumplimiento de reglas;
- ausencia de excepciones no autorizadas;
- derivación correcta;
- consistencia ante una misma condición.

#### Utility-Based Agent básico

- coherencia del ranking;
- aplicación correcta de pesos;
- selección de la alternativa con mayor puntuación válida;
- explicación consistente con los criterios.

---

## 13. LLM as a Judge

Un modelo evaluador podría revisar:

1. Si el agente comprendió la intención.
2. Si extrajo correctamente la información.
3. Si utilizó correctamente el estado interno.
4. Si repitió preguntas ya respondidas.
5. Si la conversación avanzó hacia un objetivo.
6. Si aplicó correctamente las reglas simples.
7. Si recomendó únicamente alternativas válidas.
8. Si la recomendación fue coherente con la puntuación de utilidad.
9. Si explicó de forma comprensible por qué eligió una alternativa.
10. Si inventó información.
11. Si diferenció memoria temporal y permanente.
12. Si solicitó consentimiento antes de guardar datos.
13. Si derivó correctamente los casos complejos.
14. Si la respuesta fue clara y breve.
15. Si el usuario mantuvo el control final.

El LLM evaluador no debería ser el único método de evaluación. También se deberían utilizar casos de prueba con resultados esperados y validaciones determinísticas.

---

## 14. Flujo funcional

```text
Usuario inicia la conversación
        ↓
LLM interpreta el mensaje
        ↓
Identifica intención y extrae datos
        ↓
Model-Based Reflex Agent actualiza el estado interno
        ↓
Goal-Based Agent identifica el siguiente objetivo
        ↓
¿Faltan datos obligatorios?
        ↓
Sí → Simple Reflex Agent solicita los datos faltantes
        ↓
No → Consulta catálogo, cobertura y disponibilidad
        ↓
Simple Reflex Agent aplica reglas y descarta opciones inválidas
        ↓
Utility-Based Agent básico puntúa las alternativas válidas
        ↓
Selecciona la alternativa con mayor utilidad
        ↓
LLM explica la recomendación
        ↓
Calcula una cotización cuando es posible
        ↓
¿El caso requiere intervención humana?
        ↓
Sí → Deriva a un asesor con un resumen
        ↓
No → Finaliza la consulta
        ↓
Solicita confirmación para guardar preferencias
        ↓
Actualiza memoria de largo plazo si existe consentimiento
```

### Ciclo simplificado del agente

```text
Percepción
Mensaje del usuario
        ↓
Interpretación
LLM comprende y extrae datos
        ↓
Estado
Model-Based Reflex Agent actualiza la memoria
        ↓
Objetivo
Goal-Based Agent define qué falta lograr
        ↓
Reglas
Simple Reflex Agent valida condiciones
        ↓
Utilidad
Utility-Based Agent compara alternativas
        ↓
Acción
Responder, recomendar, cotizar o derivar
```

---

## 15. Ejemplo de interacción

### Estado inicial

```json
{
  "estado": "inicio",
  "datos_faltantes": []
}
```

### Conversación

**Usuario:**

Estoy organizando un cumpleaños para unas veinte personas y necesito algo práctico.

**Procesamiento interno:**

- El LLM identifica la intención `solicitar_recomendacion`.
- Extrae la ocasión, cantidad de asistentes y preferencia.
- El Model-Based Reflex Agent actualiza el estado.
- El Goal-Based Agent detecta que faltan fecha y ubicación.
- Una regla simple indica que debe solicitar únicamente esos datos.

**Agente:**

Para revisar una alternativa adecuada, ¿en qué fecha será el cumpleaños y en qué zona se realizará?

**Usuario:**

Será el próximo sábado en Miraflores.

**Procesamiento interno:**

- El estado se actualiza con la fecha y ubicación.
- Se valida cobertura y factibilidad.
- Se consultan las alternativas disponibles.
- Se descartan las opciones que no cumplen capacidad o disponibilidad.
- Las alternativas restantes se ordenan mediante una puntuación básica de utilidad.

**Agente:**

Encontré una alternativa que podría ajustarse bien a tu reunión porque tiene capacidad para veinte personas, está disponible para la fecha indicada y coincide con tu preferencia por una opción práctica. ¿Deseas que prepare una cotización referencial?

**Usuario:**

Sí. Normalmente prefiero este tipo de opciones para mis reuniones.

**Agente:**

Prepararé la cotización con los datos de este evento. Además, ¿deseas que recuerde que normalmente prefieres opciones prácticas para futuras recomendaciones?

**Usuario:**

Sí.

**Agente:**

Listo. Guardaré esa preferencia para futuras consultas. La cotización quedará preparada con la información confirmada y, si deseas continuar con el cierre, el caso será derivado a un asesor.

### Estado final

```json
{
  "intencion": "solicitar_cotizacion",
  "ocasion": "cumpleaños",
  "asistentes": 20,
  "fecha": "proximo_sabado",
  "ubicacion": "Miraflores",
  "preferencia_actual": "alternativa_practica",
  "alternativa_recomendada": "alternativa_A",
  "estado": "cotizacion_preparada",
  "siguiente_objetivo": "derivar_para_cierre",
  "consentimiento_guardar_preferencia": true
}
```

---

## 16. Resumen ejecutivo

| Dimensión | Definición |
|---|---|
| Communication Layer | Conversacional y no conversacional |
| Domain | Ocasiones de consumo, reuniones y eventos |
| Objetivo | Recomendar, cotizar y derivar oportunidades |
| Arquitectura principal | Model-Based Reflex Agent |
| Orientación de acciones | Goal-Based Agent |
| Validaciones | Simple Reflex Agent |
| Comparación de alternativas | Utility-Based Agent básico |
| Integración de lenguaje | LLM para comprensión, extracción, explicación y resumen |
| Knowledge | Catálogo, reglas, cobertura y base de conocimiento |
| Tools | Consultar, validar, evaluar, cotizar, recordar y derivar |
| Short-Term Memory | Estado interno de la conversación actual |
| Long-Term Memory | Preferencias y fechas autorizadas |
| Autonomía | Semiautónomo y constreñido |
| Criticidad | Media – controlada |
| Control humano | Obligatorio para negociación, cierre y excepciones |
| Aprendizaje autónomo | No incluido en esta versión |
| Resultado esperado | Recomendación relevante y cotización más ágil |

---

## Conclusión

La propuesta utiliza el **Model-Based Reflex Agent** como base porque el agente necesita mantener el contexto y el estado de la conversación. El **Goal-Based Agent** permite orientar cada acción hacia una recomendación, cotización o derivación. El **Simple Reflex Agent** controla validaciones directas y restricciones, mientras que el **Utility-Based Agent básico** permite comparar las alternativas válidas.

El LLM funciona como la capa de comprensión y generación de lenguaje, pero las decisiones críticas continúan controladas mediante reglas, herramientas y fuentes estructuradas. Esta combinación permite construir un primer prototipo que demuestra los modelos revisados en clase sin requerir una arquitectura demasiado compleja.
