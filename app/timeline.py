from __future__ import annotations

import re
from datetime import datetime

from dateutil import parser

from .config import DATE_REGEX


def _parse_date(raw: str):
    try:
        return parser.parse(raw, dayfirst=True)
    except (ValueError, TypeError, OverflowError):
        return None


def build_timeline(page_rows: list[dict]) -> list[dict]:
    events = []
    for row in page_rows:
        matches = re.findall(DATE_REGEX, row["text"])
        if not matches:
            continue

        snippet = (row["text"] or "")[:280].replace("\n", " ")
        for m in matches:
            parsed = _parse_date(m)
            if not parsed:
                continue
            events.append(
                {
                    "fecha": parsed.date().isoformat(),
                    "actuacion": "Actuación detectada automáticamente",
                    "documento_fuente": row["file_name"],
                    "pagina": row["page"],
                    "fragmento": snippet,
                }
            )

    events.sort(key=lambda e: datetime.fromisoformat(e["fecha"]))
    return events
