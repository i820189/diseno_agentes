# Aplicabilidad de agentes colaborativos A2A en el proyecto

## 1. Contexto del proyecto

El proyecto consiste en un agente de ventas para ocasiones de consumo y eventos. Su función es conversar con el usuario, entender qué necesita, recopilar información como fecha, ubicación y cantidad de personas, y recomendar una alternativa.

En su versión actual, el agente puede trabajar de forma independiente y consultar herramientas internas para obtener información de productos, cobertura o disponibilidad.

Por ese motivo, considero que **A2A no es indispensable para la primera versión del proyecto**. El agente puede resolver el flujo principal utilizando su propio LLM, memoria, reglas y herramientas.

Sin embargo, A2A sí podría tener utilidad si en el futuro el agente necesita colaborar con agentes de otras empresas o plataformas.

## 2. ¿A2A aplica al proyecto?

Considero que su aplicabilidad es **futura y parcial**, no inmediata.

No aplicaría A2A para separar funciones internas como recomendación, validación o cotización. Estas actividades podrían ser realizadas por subagentes internos o por herramientas dentro de la misma aplicación, sin necesidad de utilizar un protocolo externo.

A2A sería más útil cuando el agente de ventas necesite comunicarse con un agente independiente, por ejemplo:

- un agente de un proveedor de eventos;
- un agente de logística;
- un agente de pagos;
- un agente de disponibilidad de equipos;
- un agente perteneciente a otra unidad de negocio.

En estos casos, cada agente podría haber sido desarrollado por una empresa o equipo diferente y utilizar su propia tecnología.

## 3. Ejemplo de aplicación en el proyecto

Un posible caso sería la coordinación con un proveedor externo.

El usuario podría indicar:

> Necesito una opción para un cumpleaños de treinta personas el próximo sábado en Miraflores.

El agente del proyecto recopilaría los datos y determinaría qué servicio necesita consultar.

Luego podría comunicarse mediante A2A con el agente del proveedor:

```text
Usuario
   ↓
Agente de ventas del proyecto
   ↓ A2A
Agente externo del proveedor
```

El agente externo podría responder si:

- tiene cobertura en la ubicación;
- cuenta con disponibilidad;
- puede atender la cantidad de personas;
- cuál sería el precio estimado;
- qué condiciones deben cumplirse.

El agente del proyecto recibiría esa respuesta y se la explicaría al usuario.

## 4. Posible esquema colaborativo externo

Propongo un esquema sencillo con tres participantes:

```text
                    Usuario
                       │
                       ▼
             Agente de ventas principal
                       │
            ┌──────────┴──────────┐
            │ A2A                 │ A2A
            ▼                     ▼
Agente externo de proveedor   Agente externo de logística
```

### Agente de ventas principal

Sería el agente desarrollado dentro del proyecto.

Sus funciones serían:

- entender la necesidad;
- recopilar los datos del evento;
- decidir qué agente externo consultar;
- enviar la solicitud;
- recibir la respuesta;
- presentar el resultado al usuario.

### Agente externo de proveedor

Podría encargarse de:

- consultar disponibilidad;
- validar capacidad;
- devolver precios;
- informar condiciones del servicio.

### Agente externo de logística

Podría encargarse de:

- validar cobertura;
- estimar tiempos de entrega;
- informar restricciones de acceso;
- confirmar el costo logístico.

## 5. ¿Cómo colaboraría mediante A2A?

De acuerdo con lo comprendido en clase, el agente principal no tendría que conocer cómo funciona internamente el agente externo.

Primero podría consultar su **Agent Card** para conocer sus capacidades.

Ejemplo simplificado:

```json
{
  "name": "Agente de proveedor de eventos",
  "description": "Consulta disponibilidad y precios para eventos",
  "capabilities": [
    "consultar_disponibilidad",
    "consultar_precio",
    "validar_capacidad"
  ]
}
```

Luego, el agente principal podría enviar una tarea:

```json
{
  "task_id": "TASK-001",
  "action": "consultar_disponibilidad",
  "input": {
    "fecha": "sábado",
    "ubicacion": "Miraflores",
    "asistentes": 30
  }
}
```

El agente externo podría responder:

```json
{
  "task_id": "TASK-001",
  "status": "completed",
  "output": {
    "disponible": true,
    "precio_estimado": 950,
    "requiere_confirmacion": true
  }
}
```

## 6. Gestión de estados

A2A también podría ser útil cuando la tarea no se resuelve inmediatamente.

Por ejemplo, una consulta podría pasar por estos estados:

```text
submitted
   ↓
working
   ↓
completed
```

Si falta información, podría devolver:

```text
input_required
```

Si ocurre un problema:

```text
failed
```

Esto permitiría que el agente principal conozca el avance sin acceder al funcionamiento interno del agente externo.

## 7. Diferencia con MCP

Para este proyecto entiendo la diferencia de la siguiente manera:

```text
MCP: conecta un agente con herramientas o recursos.
A2A: conecta un agente con otro agente independiente.
```

Por ejemplo:

```text
Agente de ventas
      │
      │ A2A
      ▼
Agente externo de logística
      │
      │ MCP
      ▼
Sistema de rutas y cobertura
```

El agente de logística podría utilizar MCP para consultar sus propias herramientas, mientras que nuestro agente se comunicaría con él mediante A2A.

## 8. Ventajas para el proyecto

La principal ventaja sería poder integrar servicios externos sin tener que incorporar toda su lógica dentro del agente principal.

También permitiría:

- trabajar con agentes de diferentes proveedores;
- descubrir qué capacidades ofrece cada agente;
- gestionar tareas de larga duración;
- separar responsabilidades entre empresas;
- cambiar de proveedor sin modificar todo el sistema;
- mantener privada la memoria y las herramientas de cada agente.

## 9. Limitaciones

No considero que A2A deba implementarse solamente porque el proyecto utiliza agentes.

También habría algunos retos:

- mayor complejidad técnica;
- necesidad de autenticación;
- posibles tiempos de espera;
- dependencia de agentes externos;
- manejo de errores;
- riesgo de respuestas contradictorias;
- necesidad de definir qué agente es responsable del resultado.

Además, para una primera versión académica podría ser suficiente simular esta comunicación mediante mensajes JSON, sin implementar todavía un protocolo A2A completo.

## 10. Propuesta de evolución

La implementación podría plantearse en dos etapas.

### Etapa inicial

El agente trabaja con sus propias herramientas:

```text
Usuario
   ↓
Agente de ventas
   ↓
Catálogo, cobertura y disponibilidad
```

### Extensión futura con A2A

El agente se comunica con agentes externos:

```text
Usuario
   ↓
Agente de ventas
   ├── A2A → Agente de proveedor
   ├── A2A → Agente de logística
   └── A2A → Agente de pagos
```

## 11. Conclusión

Considero que A2A no es necesario para resolver el funcionamiento interno del proyecto. La coordinación entre componentes o subagentes propios puede realizarse mediante el framework utilizado.

Su mayor aplicabilidad aparece cuando el agente de ventas necesita colaborar con agentes independientes de proveedores, operadores logísticos, plataformas de pago u otras organizaciones.

Por ello, propondría mantener la primera versión como un agente con herramientas internas y presentar A2A como una posible extensión para integrar servicios externos de forma estandarizada.

La idea principal sería:

```text
El sistema interno no necesita A2A.

A2A se utilizaría cuando nuestro agente
necesite descubrir, solicitar y recibir tareas
de agentes externos o independientes.
```
