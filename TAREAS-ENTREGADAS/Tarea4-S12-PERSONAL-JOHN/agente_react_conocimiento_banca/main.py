import os

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.utils.uuid import uuid7

from prompts import SYSTEM_PROMPT
from tools import (
    registrar_iniciativa,
    actualizar_iniciativa,
    consultar_iniciativas,
    registrar_procedimiento,
    actualizar_procedimiento,
    consultar_procedimientos,
    buscar_conocimiento,
)

TOOLS = [
    registrar_iniciativa,
    actualizar_iniciativa,
    consultar_iniciativas,
    registrar_procedimiento,
    actualizar_procedimiento,
    consultar_procedimientos,
    buscar_conocimiento,
]

agent = create_agent(
    model=f"ollama:{os.getenv('AGENTE_BANCA_MODELO', 'gemma4')}",
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)

def main() -> None:
    config = {"configurable": {"thread_id": str(uuid7())}}
    print("Agente Personal de Conocimiento de Iniciativas y Procedimientos Bancarios")
    print("Ejemplos:")
    print("- ¿Qué iniciativas están pendientes?")
    print("- Registra una iniciativa ficticia y sus personas relacionadas.")
    print("- Actualiza el estado y responsable de la iniciativa 1.")
    print("- ¿Cómo se realiza un pase a producción?")
    print("Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Usuario: ").strip()
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("Asistente: Hasta luego.")
            break
        if not user_input:
            continue
        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config,
            )
            print(f"Asistente: {result['messages'][-1].content}\n")
        except Exception as exc:
            print(f"Asistente: No pude procesar la solicitud. Detalle técnico: {exc}\n")


if __name__ == "__main__":
    main()
