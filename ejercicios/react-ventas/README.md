# Ejercicio ReAct — Agente de Ventas "Tus Eventos"

Agente que **cotiza el alquiler de un chopp/dispensador** con el patrón **ReAct**
(Reason → Act → Observe), con herramientas de **data dummy**. Inspirado en el flujo
real de **TaDa Eventos** (chopp, delivery+instalación, derivación a asesor en 48h),
pero ejecutando el plan de nuestro **system prompt** (7 datos mínimos + regla de acceso).

## Patrón ReAct
El agente **razona sus objetivos** y **consume tools** encadenando resultados:
```
 reunir datos → validar_cobertura → validar_factibilidad → consultar_disponibilidad
 → calcular_cotizacion → derivar_a_asesor
```
El resultado de una herramienta alimenta la siguiente. El plan vive en el razonamiento.

## Datos mínimos (recopila solo los faltantes; hay memoria, no repregunta)
`fecha_evento · distrito · producto · producto_capacidad · cantidad · piso · tiene_ascensor`

## Regla de acceso (dura, validada por `validar_factibilidad`)
- `piso > 2` y **sin ascensor** → **NO procede** (no se puede subir el equipo) → deriva.
- **con ascensor** → procede en cualquier piso.
- `piso <= 2` → procede.

## Herramientas (5, con data dummy)
`validar_cobertura` · `validar_factibilidad` · `consultar_disponibilidad` · `calcular_cotizacion` · `derivar_a_asesor`

## Cómo correr
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # pon tu GEMINI_API_KEY
python ventas_react.py --demo     # recorrido guiado (cotiza y deriva)
python ventas_react.py            # interactivo
```

## Tipo de agente (profile card Grupo 5)
Híbrido: **Model-Based** (memoria del estado) + **Goal-Based** (objetivos ordenados) +
**Simple Reflex** (reglas: cobertura, acceso, derivación) + **Utility básico**. La ejecución
es **ReAct** (razonar → actuar con tools → observar).
