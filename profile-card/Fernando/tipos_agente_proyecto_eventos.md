# 2. Tipo de agente

El agente se clasifica como un **agente híbrido** que combina cuatro modelos reflexivos.

## 2.1 Model-Based Reflex Agent

El **Model-Based Reflex Agent** será la arquitectura principal.

Este modelo permitirá que el agente mantenga un estado interno de la conversación y pueda recordar:

- qué información ya fue entregada;
- qué datos todavía faltan;
- qué alternativas fueron revisadas;
- qué opciones fueron descartadas;
- en qué etapa del proceso se encuentra el consumidor;
- cuál debería ser la siguiente acción.

Por ejemplo, si el usuario primero indica que está organizando un cumpleaños para veinte personas y luego señala la fecha y ubicación, el agente deberá unir estos datos dentro de un mismo estado.

### Ejemplo de estado interno

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

## 2.2 Goal-Based Agent

El agente también tendrá características de un **Goal-Based Agent**, porque sus decisiones estarán orientadas a alcanzar objetivos específicos.

El objetivo general será ayudar al consumidor a elegir una alternativa adecuada y avanzar hacia una cotización o atención humana.

Para lograrlo, el agente tendrá metas intermedias:

- identificar la intención;
- comprender la ocasión de consumo;
- completar los datos mínimos;
- validar cobertura y factibilidad;
- recomendar una alternativa;
- generar una cotización básica;
- derivar el caso cuando corresponda.

El agente utilizará el estado interno para decidir qué acción lo acerca más al objetivo.

Por ejemplo, si ya conoce la ocasión y la cantidad de asistentes, pero todavía no conoce la fecha, su siguiente acción será solicitar ese dato en lugar de realizar una recomendación incompleta.

## 2.3 Simple Reflex Agent

El agente incluirá reglas de tipo **Simple Reflex Agent** para aplicar validaciones puntuales mediante condiciones directas.

Estas reglas seguirán una lógica básica:

```text
SI ocurre una condición
ENTONCES ejecutar una acción
```

### Ejemplos

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

## 2.4 Utility-Based Agent básico

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
