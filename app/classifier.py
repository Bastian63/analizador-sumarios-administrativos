from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from .config import DATE_REGEX, DOC_TYPE_HINTS, KEYWORDS, PERSON_REGEX
from .pdf_reader import count_pages


def probable_doc_type(text: str) -> str:
    lower = text.lower()
    score = {}
    for doc_type, hints in DOC_TYPE_HINTS.items():
        score[doc_type] = sum(1 for h in hints if h in lower)
    best = max(score, key=score.get)
    return best if score[best] > 0 else "otro"


def build_document_index(pdf_path: Path, pages: list[dict]) -> dict:
    all_text = "\n".join(p["text"] for p in pages if p["file_name"] == pdf_path.name)
    dates = sorted(set(re.findall(DATE_REGEX, all_text)))
    persons = Counter(re.findall(PERSON_REGEX, all_text)).most_common(8)
    words = [kw for kw in KEYWORDS if kw.lower() in all_text.lower()]

    return {
        "archivo": pdf_path.name,
        "paginas": count_pages(pdf_path),
        "tipo_probable": probable_doc_type(all_text),
        "fechas_detectadas": ", ".join(dates[:8]),
        "personas_mencionadas": ", ".join(name for name, _ in persons),
        "palabras_clave": ", ".join(words),
    }
