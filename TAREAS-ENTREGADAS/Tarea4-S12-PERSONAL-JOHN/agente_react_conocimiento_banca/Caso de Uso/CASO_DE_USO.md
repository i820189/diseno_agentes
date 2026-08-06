# Caso de uso — Registro de una iniciativa bancaria

## Objetivo

Registrar progresivamente una iniciativa bancaria y consultar después la
información guardada. Los datos del ejemplo son ficticios y se usan únicamente
con fines académicos.

## 1. El agente solicita los datos faltantes

El usuario menciona una iniciativa llamada **Samsung Pay** relacionada con VISA
y Thales. Como faltan datos obligatorios, el agente solicita:

- Objetivo.
- Alcance.
- Estado.
- Rol de los equipos relacionados.

![El agente solicita los datos faltantes](<Captura de pantalla 2026-08-02 a la(s) 8.06.37p.m.png>)

## 2. El agente registra la iniciativa

El usuario completa la información y confirma el registro. El agente utiliza
`registrar_iniciativa` y guarda:

- Nombre: Samsung Pay.
- Objetivo: habilitar pagos mediante celulares Samsung.
- Alcance: realizar configuraciones en el equipo ficticio Xpay.
- Estado: En desarrollo.
- Equipos relacionados: VISA y Thales.

La iniciativa queda registrada con el ID 1.

![El agente registra la iniciativa](<Captura de pantalla 2026-08-02 a la(s) 8.06.57p.m.png>)

## 3. El agente recupera la información

El usuario pregunta: **“dame todo lo que sepas de Samsung Pay”**.

El agente utiliza `consultar_iniciativas` y responde con el estado, objetivo,
alcance, equipos relacionados y los campos todavía no informados.

![El agente consulta la iniciativa](<Captura de pantalla 2026-08-02 a la(s) 8.07.21p.m.png>)

## Flujo ReAct demostrado

```text
Usuario proporciona información
        ↓
El agente identifica los datos faltantes
        ↓
Acción: registrar_iniciativa
        ↓
Observación: iniciativa registrada con ID 1
        ↓
Acción: consultar_iniciativas
        ↓
Observación: información recuperada
        ↓
Respuesta final
```

## Resultado

El caso demuestra que el agente puede recibir información en varios mensajes,
registrarla mediante una herramienta y recuperarla posteriormente. Así, el
conocimiento de las iniciativas queda organizado para futuras consultas.
