# Agente de recomendaciones — MVP v0.2

Versión pequeña basada en `Agentic_Profile_Card_v3.0_Codex.md` y organizada como los
ejemplos de agentes con LangChain, LangGraph y Ollama.

## Tipos de agente que demuestra

No son cuatro agentes independientes. Es el **monoagente híbrido** pedido por el MD:

- **Model-Based Reflex (principal):** `EstadoRecomendacion` conserva el modelo interno y
  `prompt_con_modelo_interno` lo inyecta en cada paso.
- **Simple Reflex:** `aplicar_reglas_reflejo` decide por reglas si pregunta, valida o deriva.
- **Goal-Based:** `current_goal` guía la secuencia hasta recomendar o derivar.
- **Utility-Based:** `evaluar_alternativas` filtra y compara con pesos fijos.

## Estructura

```text
agente/
├── agent.py          # create_agent + prompt dinámico
├── domain.py         # catálogo mock y utilidad sin dependencia del LLM
├── main.py           # conversación por terminal
├── models.py         # modelo interno / estado
├── tools.py          # tools, reglas y función de utilidad
├── system_prompt.md  # instrucciones versionadas fuera del código
└── tests/             # pruebas determinísticas
```

## Instalación y ejecución

Requiere Python 3.11+ y Ollama:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r agente/requirements.txt
ollama pull llama3.2
python3 -m agente
```

Conversación sugerida:

```text
Necesito algo práctico para un cumpleaños.
Somos 20, será el 2026-08-15 en Miraflores.
```

## Tools del MVP

- `actualizar_modelo_interno`: registra hechos y mantiene memoria de sesión.
- `aplicar_reglas_reflejo`: ejecuta reglas simples obligatorias.
- `validar_cobertura`: consulta una fuente operativa simulada.
- `evaluar_alternativas`: filtra, calcula utilidad y ordena opciones.

El catálogo y la cobertura son mocks. No se implementan todavía cotización, memoria a
largo plazo, RAG ni APIs reales.

## Pruebas

Con las dependencias instaladas:

```bash
python3 -m unittest discover -s agente/tests -v
```
