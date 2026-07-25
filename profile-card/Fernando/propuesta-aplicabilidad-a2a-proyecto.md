# Aplicabilidad de agentes colaborativos A2A en el proyecto

## 1. Contexto del proyecto

El proyecto consiste en un agente de ventas para ocasiones de consumo y eventos. Su función es conversar con el usuario, entender qué necesita, recopilar información como fecha, ubicación y cantidad de personas, y recomendar una alternativa.

En su versión actual, el agente puede trabajar de forma independiente y consultar herramientas internas para obtener información de productos, cobertura o disponibilidad.

Por ese motivo, considero que **A2A no es indispensable para la primera versión del proyecto**. El agente puede resolver el flujo principal utilizando su propio LLM, memoria, reglas y herramientas.

Sin embargo, A2A sí podría tener utilidad si en el futuro el agente necesita colaborar con agentes de otras empresas o plataformas.

> Como referencia, A2A es un estándar abierto lanzado por Google (2025) y hoy gobernado por la Linux Foundation, con más de 150 organizaciones y soporte en las plataformas de Google, AWS y Microsoft. Es una tecnología madura, pero eso no la vuelve obligatoria: se adopta por necesidad, no por moda.

## 2. ¿A2A aplica al proyecto?

Considero que su aplicabilidad es **futura y parcial**, no inmediata.

No aplicaría A2A para separar funciones internas como recomendación, validación o cotización. Estas actividades podrían ser realizadas por subagentes internos o por herramientas dentro de la misma aplicación, sin necesidad de utilizar un protocolo externo.

Aquí conviene hacer dos precisiones para no sobre-diseñar:

- **Multiagente no es lo mismo que A2A.** Se pueden tener varios agentes cooperando dentro del mismo stack (por ejemplo con LangGraph) sin A2A. A2A recién aparece cuando se cruzan fronteras de organización o de proveedor.
- **A2A no es lo mismo que MCP.** MCP conecta un agente con sus herramientas y datos; A2A conecta agentes entre sí. Se complementan, no compiten. Por eso, no todo servicio externo es A2A: un pago o una consulta de disponibilidad suelen ser una API o una herramienta MCP (deterministas), no un agente que razona.

A2A sería más útil cuando el agente de ventas necesite comunicarse con un agente independiente, por ejemplo:

- un agente de un proveedor de eventos;
- un agente de logística;
- un agente de pagos;
- un agente de disponibilidad de equipos;
- un agente perteneciente a otra unidad de negocio.

En estos casos, cada agente podría haber sido desarrollado por una empresa o equipo diferente y utilizar su propia tecnología, y solo se justifica A2A si esa contraparte es realmente un agente autónomo que razona.

## 3. Colaboración por medios externos (paso previo a A2A)

Antes de A2A, el enunciado pide un esquema de colaboración **por medios externos**. En la sesión eso se definió como variables y archivos (el laboratorio fue un agente que persiste a un archivo y un segundo agente que lo lee y lo analiza).

Aplicado a este proyecto, un esquema sencillo sería separar la venta de la post-venta coordinándolas por un archivo compartido:

```text
Agente de ventas ──escribe──► pedido.json ──lee──► Agente de post-venta
   (cotiza y cierra)          { estado:              (confirma, recordatorio,
                                "cotizado" }          seguimiento)
```

Cada agente corre por su lado y no comparte memoria ni herramientas; el archivo funciona como buzón. El campo `estado` (cotizado → confirmado → cerrado) permite que el segundo agente sepa qué falta sin acceder al interior del primero. Es un desacople barato, auditable y sin protocolo, y es el paso natural antes de considerar A2A.

## 4. Ejemplo de aplicación en el proyecto

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

## 5. Posible esquema colaborativo externo

Propongo un esquema sencillo con tres participantes (dejando el pago como una API o herramienta MCP, ya que es un servicio determinista, no un agente que razona):

```text
                    Usuario
                       │
                       ▼
             Agente de ventas principal
            ┌──────────┼────────────────┐
            │ A2A      │ A2A             │ API / MCP
            ▼          ▼                 ▼
Agente externo de   Agente externo de   Pasarela de pagos
   proveedor           logística        (servicio determinista)
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

## 6. ¿Cómo colaboraría mediante A2A?

De acuerdo con lo comprendido en clase, el agente principal no tendría que conocer cómo funciona internamente el agente externo.

Primero podría consultar su **Agent Card** para conocer sus capacidades.

> Los JSON siguientes son un ejemplo simplificado; el A2A real transporta sobre JSON-RPC 2.0 / HTTP(S) con SSE para streaming, publica la Agent Card en `/.well-known/` y usa autenticación.

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

## 7. Gestión de estados

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

Un punto adicional de seguridad: la respuesta de un agente externo (de otra empresa) es entrada no confiable y podría traer instrucciones ocultas (prompt injection). Debe tratarse como dato, nunca como instrucción: validar contra esquema, delimitar el contenido y no dejar que altere el comportamiento del agente principal.

Además, para una primera versión académica podría ser suficiente simular esta comunicación mediante mensajes JSON, sin implementar todavía un protocolo A2A completo.

## 10. Propuesta de evolución

La implementación podría plantearse en tres etapas.

### Etapa inicial

El agente trabaja con sus propias herramientas:

```text
Usuario
   ↓
Agente de ventas
   ↓
Catálogo, cobertura y disponibilidad
```

### Etapa intermedia (medios externos)

Dos agentes propios se coordinan por un archivo compartido:

```text
Usuario
   ↓
Agente de ventas
   ↓ (archivo)
pedido.json → Agente de post-venta
```

### Extensión futura con A2A

El agente se comunica con agentes externos (el pago queda como API/MCP):

```text
Usuario
   ↓
Agente de ventas
   ├── A2A → Agente de proveedor
   ├── A2A → Agente de logística
   └── API/MCP → Pasarela de pagos
```

## 11. Conclusión

Considero que A2A no es necesario para resolver el funcionamiento interno del proyecto. La coordinación entre componentes o subagentes propios puede realizarse mediante el framework utilizado, y la colaboración entre dos procesos propios puede resolverse por medios externos (un archivo compartido).

Su mayor aplicabilidad aparece cuando el agente de ventas necesita colaborar con agentes independientes de proveedores, operadores logísticos u otras organizaciones, y ni siquiera para todo, porque un servicio determinista (como el pago) es una API o herramienta MCP, no A2A.

Por ello, propondría mantener la primera versión como un agente con herramientas internas, plantear la colaboración por archivo compartido como evolución natural, y presentar A2A como una posible extensión para integrar servicios externos que razonan de forma estandarizada.

La idea principal sería:

```text
El sistema interno no necesita A2A.
Entre procesos propios se usa un medio externo (archivo).
A2A se utilizaría cuando nuestro agente necesite descubrir, solicitar y recibir
tareas de agentes externos o independientes de otras organizaciones.
```
