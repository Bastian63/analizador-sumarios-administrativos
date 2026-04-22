from __future__ import annotations

from pathlib import Path

import fitz


def extract_text_by_page(pdf_path: Path) -> list[dict]:
    """Extrae texto por página y conserva referencia a archivo/página."""
    rows: list[dict] = []
    doc = fitz.open(pdf_path)
    try:
        for i, page in enumerate(doc, start=1):
            rows.append(
                {
                    "file_name": pdf_path.name,
                    "file_path": str(pdf_path),
                    "page": i,
                    "text": page.get_text("text").strip(),
                }
            )
    finally:
        doc.close()
    return rows


def count_pages(pdf_path: Path) -> int:
    doc = fitz.open(pdf_path)
    try:
        return len(doc)
    finally:
        doc.close()
