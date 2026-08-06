import json
import os
import tempfile
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from langchain.tools import tool

BASE_DIR = Path(__file__).parent
INICIATIVAS_FILE = BASE_DIR / "iniciativas.json"
PROCEDIMIENTOS_FILE = BASE_DIR / "procedimientos.json"
CONOCIMIENTO_DIR = BASE_DIR / "conocimiento"

ESTADOS_VALIDOS = {
    "Idea",
    "En análisis",
    "En desarrollo",
    "En pruebas",
    "Producción",
    "Pausada",
    "Finalizada",
}
ESTADOS_CERRADOS = {"Producción", "Finalizada"}


def _leer_json(ruta: Path) -> list[dict]:
    if not ruta.exists():
        return []

    try:
        contenido = ruta.read_text(encoding="utf-8").strip()
        datos = json.loads(contenido) if contenido else []
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(f"No se pudo leer correctamente {ruta.name}: {exc}") from exc

    if not isinstance(datos, list):
        raise RuntimeError(f"{ruta.name} debe contener una lista JSON.")
    return datos


def _guardar_json(ruta: Path, datos: list[dict]) -> None:
    """Escribe de forma atómica para no dejar un JSON parcial."""
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=ruta.parent, delete=False
        ) as archivo:
            temporal = Path(archivo.name)
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
        os.replace(temporal, ruta)
    except OSError as exc:
        if temporal and temporal.exists():
            temporal.unlink()
        raise RuntimeError(f"No se pudo guardar {ruta.name}: {exc}") from exc


def _normalizar(texto: str) -> str:
    sin_tildes = "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )
    return " ".join(sin_tildes.casefold().split())


def _validar_texto(nombre: str, valor: str) -> Optional[str]:
    if not valor or not valor.strip():
        return f"El campo '{nombre}' es obligatorio."
    return None


def _validar_estado(estado: str) -> Optional[str]:
    coincidencias = {
        _normalizar(permitido): permitido for permitido in ESTADOS_VALIDOS
    }
    if _normalizar(estado) not in coincidencias:
        return "Estado inválido. Usa uno de estos valores: " + ", ".join(
            sorted(ESTADOS_VALIDOS)
        )
    return None


def _estado_canonico(estado: str) -> str:
    return {_normalizar(item): item for item in ESTADOS_VALIDOS}[_normalizar(estado)]


def _validar_fecha(fecha: str) -> Optional[str]:
    if fecha in {"", "No informada"}:
        return None
    try:
        date.fromisoformat(fecha)
    except ValueError:
        return "La fecha de entrega debe usar el formato YYYY-MM-DD o 'No informada'."
    return None


def _personas_validas(personas: list[dict[str, str]]) -> Optional[str]:
    for persona in personas:
        if not all(str(persona.get(campo, "")).strip() for campo in ("nombre", "rol", "relacion")):
            return "Cada persona relacionada debe incluir nombre, rol y relación."
    return None


@tool
def registrar_iniciativa(
    nombre: str,
    objetivo: str,
    alcance: str,
    estado: str,
    responsable: str = "No informado",
    fecha_entrega: str = "No informada",
    dependencias: Optional[list[str]] = None,
    decisiones: Optional[list[str]] = None,
    documentos_relacionados: Optional[list[str]] = None,
    procedimientos_relacionados: Optional[list[int]] = None,
    personas_relacionadas: Optional[list[dict[str, str]]] = None,
    fuente: str = "Información proporcionada por el usuario",
) -> str:
    """Registra una iniciativa bancaria ficticia y evita nombres duplicados.

    Cada persona relacionada debe contener nombre, rol y relacion.
    """
    for campo, valor in (
        ("nombre", nombre),
        ("objetivo", objetivo),
        ("alcance", alcance),
        ("estado", estado),
    ):
        error = _validar_texto(campo, valor)
        if error:
            return error
    if error := _validar_estado(estado):
        return error
    if error := _validar_fecha(fecha_entrega):
        return error

    personas = personas_relacionadas or []
    if error := _personas_validas(personas):
        return error

    iniciativas = _leer_json(INICIATIVAS_FILE)
    if any(_normalizar(item.get("nombre", "")) == _normalizar(nombre) for item in iniciativas):
        return f"Ya existe una iniciativa con el nombre '{nombre.strip()}'."

    nuevo_id = max((item.get("id", 0) for item in iniciativas), default=0) + 1
    iniciativa = {
        "id": nuevo_id,
        "nombre": nombre.strip(),
        "objetivo": objetivo.strip(),
        "alcance": alcance.strip(),
        "estado": _estado_canonico(estado),
        "responsable": responsable.strip() or "No informado",
        "fecha_entrega": fecha_entrega.strip() or "No informada",
        "dependencias": dependencias or [],
        "decisiones": decisiones or [],
        "documentos_relacionados": documentos_relacionados or [],
        "procedimientos_relacionados": procedimientos_relacionados or [],
        "personas_relacionadas": personas,
        "fuente": fuente.strip() or "Información proporcionada por el usuario",
        "actualizado_en": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    iniciativas.append(iniciativa)
    _guardar_json(INICIATIVAS_FILE, iniciativas)
    return f"Iniciativa registrada con ID {nuevo_id}: {nombre.strip()}. Estado: {iniciativa['estado']}."


@tool
def actualizar_iniciativa(
    iniciativa_id: int,
    objetivo: Optional[str] = None,
    alcance: Optional[str] = None,
    estado: Optional[str] = None,
    responsable: Optional[str] = None,
    fecha_entrega: Optional[str] = None,
    dependencias: Optional[list[str]] = None,
    decisiones: Optional[list[str]] = None,
    documentos_relacionados: Optional[list[str]] = None,
    procedimientos_relacionados: Optional[list[int]] = None,
    personas_relacionadas: Optional[list[dict[str, str]]] = None,
    fuente: Optional[str] = None,
) -> str:
    """Actualiza uno o varios campos de una iniciativa en una sola operación."""
    cambios = {
        "objetivo": objetivo,
        "alcance": alcance,
        "estado": estado,
        "responsable": responsable,
        "fecha_entrega": fecha_entrega,
        "dependencias": dependencias,
        "decisiones": decisiones,
        "documentos_relacionados": documentos_relacionados,
        "procedimientos_relacionados": procedimientos_relacionados,
        "personas_relacionadas": personas_relacionadas,
        "fuente": fuente,
    }
    cambios = {campo: valor for campo, valor in cambios.items() if valor is not None}
    if not cambios:
        return "No se indicó ningún campo para actualizar."
    if estado is not None and (error := _validar_estado(estado)):
        return error
    if fecha_entrega is not None and (error := _validar_fecha(fecha_entrega)):
        return error
    if personas_relacionadas is not None and (error := _personas_validas(personas_relacionadas)):
        return error
    for campo in ("objetivo", "alcance", "responsable", "fuente"):
        if campo in cambios and not str(cambios[campo]).strip():
            return f"El campo '{campo}' no puede quedar vacío."

    iniciativas = _leer_json(INICIATIVAS_FILE)
    for iniciativa in iniciativas:
        if iniciativa.get("id") == iniciativa_id:
            if estado is not None:
                cambios["estado"] = _estado_canonico(estado)
            iniciativa.update(cambios)
            iniciativa["actualizado_en"] = datetime.now().astimezone().isoformat(timespec="seconds")
            _guardar_json(INICIATIVAS_FILE, iniciativas)
            return f"Iniciativa {iniciativa_id} actualizada. Campos: {', '.join(cambios)}."
    return f"No se encontró una iniciativa con ID {iniciativa_id}."


@tool
def consultar_iniciativas(
    texto_busqueda: str = "",
    estado: str = "",
    solo_pendientes: bool = False,
) -> str:
    """Consulta iniciativas. Pendiente significa estado distinto de Producción y Finalizada."""
    iniciativas = _leer_json(INICIATIVAS_FILE)
    if texto_busqueda.strip():
        termino = _normalizar(texto_busqueda)
        iniciativas = [
            item for item in iniciativas if termino in _normalizar(json.dumps(item, ensure_ascii=False))
        ]
    if estado.strip():
        if error := _validar_estado(estado):
            return error
        esperado = _normalizar(_estado_canonico(estado))
        iniciativas = [item for item in iniciativas if _normalizar(item.get("estado", "")) == esperado]
    if solo_pendientes:
        cerrados = {_normalizar(item) for item in ESTADOS_CERRADOS}
        iniciativas = [item for item in iniciativas if _normalizar(item.get("estado", "")) not in cerrados]
    if not iniciativas:
        return "No se encontraron iniciativas con los criterios indicados."

    bloques = []
    for item in iniciativas:
        personas = ", ".join(
            f"{p['nombre']} ({p['rol']}: {p['relacion']})"
            for p in item.get("personas_relacionadas", [])
        ) or "No informadas"
        bloques.append(
            f"ID {item['id']} | {item['nombre']} | Estado: {item['estado']} | "
            f"Responsable: {item.get('responsable', 'No informado')} | "
            f"Fecha: {item.get('fecha_entrega', 'No informada')}\n"
            f"Objetivo: {item['objetivo']}\nAlcance: {item['alcance']}\n"
            f"Personas relacionadas: {personas}\n"
            f"Dependencias: {item.get('dependencias', [])}\n"
            f"Decisiones: {item.get('decisiones', [])}\n"
            f"Documentos: {item.get('documentos_relacionados', [])}\n"
            f"Procedimientos: {item.get('procedimientos_relacionados', [])}\n"
            f"Fuente: {item.get('fuente', 'No informada')}"
        )
    return "\n\n---\n\n".join(bloques)


def _estado_documentacion(procedimiento: dict) -> str:
    obligatorios = (
        "equipo_responsable", "objetivo", "prerrequisitos", "pasos",
        "sistema", "ambiente", "tecnologia", "fuente", "version_o_fecha",
    )
    return "Documentado" if all(str(procedimiento.get(campo, "")).strip() for campo in obligatorios) else "Borrador"


@tool
def registrar_procedimiento(
    nombre: str,
    equipo_responsable: str = "",
    objetivo: str = "",
    prerrequisitos: str = "",
    pasos: str = "",
    sistema: str = "",
    ambiente: str = "",
    tecnologia: str = "",
    evidencias: Optional[list[str]] = None,
    fuente: str = "",
    version_o_fecha: str = "",
    iniciativas_relacionadas: Optional[list[int]] = None,
) -> str:
    """Registra un procedimiento único. Si faltan datos queda como Borrador."""
    if error := _validar_texto("nombre", nombre):
        return error
    procedimientos = _leer_json(PROCEDIMIENTOS_FILE)
    if any(_normalizar(item.get("nombre", "")) == _normalizar(nombre) for item in procedimientos):
        return f"Ya existe un procedimiento con el nombre '{nombre.strip()}'."
    nuevo_id = max((item.get("id", 0) for item in procedimientos), default=0) + 1
    procedimiento = {
        "id": nuevo_id,
        "nombre": nombre.strip(),
        "equipo_responsable": equipo_responsable.strip(),
        "objetivo": objetivo.strip(),
        "prerrequisitos": prerrequisitos.strip(),
        "pasos": pasos.strip(),
        "sistema": sistema.strip(),
        "ambiente": ambiente.strip(),
        "tecnologia": tecnologia.strip(),
        "evidencias": evidencias or [],
        "fuente": fuente.strip(),
        "version_o_fecha": version_o_fecha.strip(),
        "iniciativas_relacionadas": iniciativas_relacionadas or [],
        "actualizado_en": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    procedimiento["estado_documentacion"] = _estado_documentacion(procedimiento)
    procedimientos.append(procedimiento)
    _guardar_json(PROCEDIMIENTOS_FILE, procedimientos)
    return (
        f"Procedimiento registrado con ID {nuevo_id}: {nombre.strip()}. "
        f"Estado de documentación: {procedimiento['estado_documentacion']}."
    )


@tool
def actualizar_procedimiento(
    procedimiento_id: int,
    equipo_responsable: Optional[str] = None,
    objetivo: Optional[str] = None,
    prerrequisitos: Optional[str] = None,
    pasos: Optional[str] = None,
    sistema: Optional[str] = None,
    ambiente: Optional[str] = None,
    tecnologia: Optional[str] = None,
    evidencias: Optional[list[str]] = None,
    fuente: Optional[str] = None,
    version_o_fecha: Optional[str] = None,
    iniciativas_relacionadas: Optional[list[int]] = None,
) -> str:
    """Actualiza uno o varios campos y recalcula si el procedimiento es borrador."""
    cambios = {
        "equipo_responsable": equipo_responsable,
        "objetivo": objetivo,
        "prerrequisitos": prerrequisitos,
        "pasos": pasos,
        "sistema": sistema,
        "ambiente": ambiente,
        "tecnologia": tecnologia,
        "evidencias": evidencias,
        "fuente": fuente,
        "version_o_fecha": version_o_fecha,
        "iniciativas_relacionadas": iniciativas_relacionadas,
    }
    cambios = {campo: valor for campo, valor in cambios.items() if valor is not None}
    if not cambios:
        return "No se indicó ningún campo para actualizar."
    procedimientos = _leer_json(PROCEDIMIENTOS_FILE)
    for procedimiento in procedimientos:
        if procedimiento.get("id") == procedimiento_id:
            for campo, valor in cambios.items():
                procedimiento[campo] = valor.strip() if isinstance(valor, str) else valor
            procedimiento["estado_documentacion"] = _estado_documentacion(procedimiento)
            procedimiento["actualizado_en"] = datetime.now().astimezone().isoformat(timespec="seconds")
            _guardar_json(PROCEDIMIENTOS_FILE, procedimientos)
            return (
                f"Procedimiento {procedimiento_id} actualizado. "
                f"Estado de documentación: {procedimiento['estado_documentacion']}."
            )
    return f"No se encontró un procedimiento con ID {procedimiento_id}."


@tool
def consultar_procedimientos(texto_busqueda: str = "") -> str:
    """Busca procedimientos registrados, incluyendo borradores con advertencia."""
    procedimientos = _leer_json(PROCEDIMIENTOS_FILE)
    if texto_busqueda.strip():
        palabras = [_normalizar(p) for p in texto_busqueda.split() if len(p) > 2]
        procedimientos = [
            item for item in procedimientos
            if any(palabra in _normalizar(json.dumps(item, ensure_ascii=False)) for palabra in palabras)
        ]
    if not procedimientos:
        return "No se encontró un procedimiento documentado con ese criterio."
    bloques = []
    for item in procedimientos:
        advertencia = (
            "ADVERTENCIA: borrador; no debe considerarse un procedimiento oficial.\n"
            if item.get("estado_documentacion") == "Borrador" else ""
        )
        bloques.append(
            f"{advertencia}ID: {item['id']}\nProcedimiento: {item['nombre']}\n"
            f"Estado de documentación: {item.get('estado_documentacion', 'Borrador')}\n"
            f"Equipo responsable: {item.get('equipo_responsable') or 'No informado'}\n"
            f"Objetivo: {item.get('objetivo') or 'No informado'}\n"
            f"Prerrequisitos: {item.get('prerrequisitos') or 'No informados'}\n"
            f"Pasos:\n{item.get('pasos') or 'No informados'}\n"
            f"Sistema: {item.get('sistema') or 'No informado'} | "
            f"Ambiente: {item.get('ambiente') or 'No informado'} | "
            f"Tecnología: {item.get('tecnologia') or 'No informada'}\n"
            f"Evidencias: {item.get('evidencias', [])}\n"
            f"Fuente: {item.get('fuente') or 'No informada'}\n"
            f"Versión/fecha: {item.get('version_o_fecha') or 'No informada'}"
        )
    return "\n\n---\n\n".join(bloques)


@tool
def buscar_conocimiento(consulta: str) -> str:
    """Busca por palabras relevantes en archivos Markdown y TXT locales."""
    palabras = {
        _normalizar(palabra.strip("¿?¡!.,:;"))
        for palabra in consulta.split()
        if len(palabra.strip("¿?¡!.,:;")) > 3
    }
    if not palabras:
        return "La consulta debe incluir al menos una palabra relevante."
    resultados = []
    if not CONOCIMIENTO_DIR.exists():
        return "No existe el directorio de conocimiento."
    for ruta in sorted(CONOCIMIENTO_DIR.rglob("*")):
        if ruta.is_file() and ruta.suffix.lower() in {".md", ".txt"}:
            try:
                contenido = ruta.read_text(encoding="utf-8")
            except OSError:
                continue
            texto = _normalizar(f"{ruta.name} {contenido}")
            coincidencias = sum(palabra in texto for palabra in palabras)
            if coincidencias:
                resultados.append((coincidencias, ruta, contenido.strip()[:1500]))
    if not resultados:
        return (
            "No se encontró información documentada en la base local. "
            "No existe evidencia suficiente; solicita una fuente adicional."
        )
    resultados.sort(key=lambda item: (-item[0], str(item[1])))
    return "\n\n---\n\n".join(
        f"Fuente: {Path('conocimiento') / ruta.relative_to(CONOCIMIENTO_DIR)}\nContenido:\n{fragmento}"
        for _, ruta, fragmento in resultados[:5]
    )
