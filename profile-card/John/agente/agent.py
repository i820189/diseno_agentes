"""Construcción del monoagente híbrido con LangChain/LangGraph."""

from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt

from .models import EstadoRecomendacion
from .tools import TOOLS


SYSTEM_PROMPT = Path(__file__).with_name("system_prompt.md").read_text(encoding="utf-8")


@dynamic_prompt
def prompt_con_modelo_interno(request: ModelRequest) -> str:
    """Model-Based Reflex: inyecta el mundo conocido antes de cada decisión."""
    estado = request.state
    resumen = {
        "occasion": estado.get("occasion"),
        "attendees": estado.get("attendees"),
        "event_date": estado.get("event_date"),
        "location": estado.get("location"),
        "preferences": estado.get("preferences", []),
        "missing_fields": estado.get("missing_fields", []),
        "coverage_status": estado.get("coverage_status"),
        "current_goal": estado.get("current_goal", "IDENTIFY_INTENT"),
    }
    return f"{SYSTEM_PROMPT}\n\n## MODELO INTERNO ACTUAL\n{resumen}"


agent = create_agent(
    model="ollama:llama3.2",
    tools=TOOLS,
    middleware=[prompt_con_modelo_interno],
    state_schema=EstadoRecomendacion,
)

