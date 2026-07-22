"""Interfaz de terminal, equivalente al main de los ejemplos."""

from uuid import uuid4

from .agent import agent
from .models import estado_inicial


def conversar() -> None:
    estado = estado_inicial(str(uuid4()))
    print("Agente: Hola. Cuéntame qué ocasión estás organizando.")
    while True:
        mensaje = input("\nTú (o 'salir'): ").strip()
        if mensaje.lower() == "salir":
            break
        entrada = {**estado, "messages": estado["messages"] + [{"role": "user", "content": mensaje}]}
        estado = agent.invoke(entrada)
        print(f"Agente: {estado['messages'][-1].content}")


if __name__ == "__main__":
    conversar()

