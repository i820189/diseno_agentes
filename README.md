# Diseño e Implementación de Agentes IA — Entregables

Repositorio de entregables del programa de posgrado.
**Proyecto elegido:** Agente de Ventas **“Tus Eventos”** — empresa ficticia que ofrece
dispensadores de bebidas y paquetes para eventos.

## Estructura
```
profile-card/
  agente-ventas-tus-eventos.md      # Profile Card base (system prompt del agente)
tareas/
  sesion-09-memoria-contextual.md   # contexto + rúbrica · Tarea S09
  sesion-10-agentes-reflexivos.md   # contexto + rúbrica · Tarea S10
```

## Flujo de trabajo (ramas → main)
Cada tarea se trabaja en **su propia rama** y al final se integra a `main`:

| Rama | Tarea | Deadline |
|------|-------|----------|
| `sesion-09` | Agentes con Memoria Contextual | 17/07 |
| `sesion-10` | Agentes Reflexivos | 22/07 |

```bash
git checkout sesion-09   # trabajar la tarea de memoria
git checkout sesion-10   # trabajar la tarea de reflex agents
# al terminar cada una → merge a main
```

## Estado de entregables
| Tarea | Entrega | Formato | Puntos | Estado |
|-------|---------|---------|:------:|:------:|
| **S09** · Memoria contextual | 17/07 | Imagen | 20 | 🔨 rama `sesion-09` |
| **S10** · Agentes reflexivos | 22/07 | Imagen + script Python (LangChain) | 20 | 🔨 rama `sesion-10` |

> Por ahora este repo contiene **solo el contexto** (Profile Card base + rúbricas).
> El código y los Profile Cards finales se agregan luego, cada uno en su rama.
