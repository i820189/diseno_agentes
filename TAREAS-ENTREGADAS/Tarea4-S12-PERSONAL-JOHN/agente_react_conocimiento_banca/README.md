# Agente Personal de Conocimiento de Iniciativas y Procedimientos Bancarios

## Necesidad personal

Registrar progresivamente el conocimiento sobre iniciativas pendientes,
procedimientos bancarios y personas relacionadas, porque diariamente necesito
recuperar esta información para resolver consultas e inconvenientes de mi trabajo.

Este proyecto es una demostración académica con datos ficticios. No contiene ni
debe recibir información confidencial de una entidad bancaria.

## Objetivo

Implementar un agente ReAct personal con LangChain que seleccione herramientas
para registrar, actualizar y consultar conocimiento local sobre iniciativas y
procedimientos bancarios, sin inventar información que no esté documentada.

## Alcance de la tarea

- Registrar iniciativas y evitar nombres duplicados.
- Guardar objetivo, alcance, estado, responsable, fecha, dependencias, decisiones,
  documentos, procedimientos y personas relacionadas.
- Actualizar varios campos de una iniciativa en una operación.
- Consultar por texto, estado o iniciativas pendientes.
- Registrar procedimientos sin duplicar nombres y actualizar el registro existente.
- Diferenciar procedimientos `Borrador` y `Documentado`.
- Buscar conocimiento en archivos Markdown y TXT locales.
- Mantener el contexto de una sesión mediante `InMemorySaver`.

Una iniciativa está pendiente cuando su estado no es `Producción` ni `Finalizada`.
Los estados válidos son: `Idea`, `En análisis`, `En desarrollo`, `En pruebas`,
`Producción`, `Pausada` y `Finalizada`.

Cada persona relacionada tiene esta estructura:

```json
{"nombre": "Ana Torres", "rol": "Líder funcional", "relacion": "Responsable de validación"}
```

Un procedimiento incompleto se guarda como `Borrador` y se muestra con una
advertencia. Pasa automáticamente a `Documentado` cuando cuenta con equipo,
objetivo, prerrequisitos, pasos, sistema, ambiente, tecnología, fuente y versión.

## Flujo ReAct

```text
Solicitud del usuario
        ↓
El agente selecciona una herramienta
        ↓
La herramienta lee o modifica el conocimiento local
        ↓
El agente observa el resultado y responde
```

El agente no expone razonamiento privado. La evidencia del patrón ReAct es la
selección y ejecución de herramientas para completar cada solicitud.

## Instalación y ejecución

```bash
ollama pull gemma4
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Ollama debe estar ejecutándose antes de iniciar el agente.
Se utiliza `gemma4` de forma predeterminada porque se verificó su ejecución de
herramientas con este proyecto. Puede elegirse otro modelo compatible mediante:

```bash
AGENTE_BANCA_MODELO=nombre_del_modelo python main.py
```

El modelo seleccionado debe soportar llamadas de herramientas; generar una
llamada como texto no completa el ciclo ReAct.

## Ejemplos

```text
Registra la iniciativa ficticia Billetera Digital, cuyo objetivo es facilitar
pagos, con alcance de piloto interno y estado En análisis. Relaciona a Ana Torres,
líder funcional y responsable de validación.

¿Qué iniciativas están pendientes?

Actualiza la iniciativa 1 al estado En pruebas y asigna como responsable al
Equipo Digital.

Registra como borrador el procedimiento Pase a producción.

¿Cómo se realiza un pase a producción?
```

## Persistencia

Las iniciativas y procedimientos se guardan en `iniciativas.json` y
`procedimientos.json`. Los documentos consultables se encuentran en
`conocimiento/`.

## Fuera del alcance

Esta entrega no procesa PDF, Word, Excel, presentaciones, grabaciones ni video;
tampoco implementa RAG vectorial, sistemas internos, arquitectura multiagente o
funcionalidades de producción bancaria.

## Transparencia sobre inteligencia artificial

Se utilizó inteligencia artificial generativa como apoyo para revisar el código,
estructurar la documentación y detectar mejoras. La definición de la necesidad,
la validación del funcionamiento y la responsabilidad sobre la entrega
corresponden al autor.
