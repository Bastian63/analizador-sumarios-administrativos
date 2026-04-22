from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "data" / "output"

DATE_REGEX = r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b"
PERSON_REGEX = r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b"

DOC_TYPE_HINTS = {
    "resolucion": ["resuelvo", "resolución", "resolucion", "visto"],
    "formulacion_de_cargos": ["formulación de cargos", "cargo", "imputa"],
    "descargos": ["descargos", "defensa", "alegaciones"],
    "declaracion": ["declara", "testigo", "declaración"],
    "notificacion": ["notifica", "notificación", "cédula"],
    "informe": ["informe", "fiscal"],
}

KEYWORDS = [
    "cargo",
    "notificación",
    "descargos",
    "prueba",
    "resolución",
    "sumario",
    "funcionario",
    "fiscal",
]
