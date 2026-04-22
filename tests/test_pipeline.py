from pathlib import Path

import fitz

from app.classifier import build_document_index
from app.pdf_reader import extract_text_by_page
from app.timeline import build_timeline


def _create_pdf(path: Path, texts: list[str]):
    doc = fitz.open()
    for t in texts:
        page = doc.new_page()
        page.insert_text((72, 72), t)
    doc.save(path)
    doc.close()


def test_extract_text_by_page(tmp_path):
    pdf = tmp_path / "test.pdf"
    _create_pdf(pdf, ["Primera página", "Segunda página"])

    rows = extract_text_by_page(pdf)

    assert len(rows) == 2
    assert rows[0]["page"] == 1
    assert "Primera" in rows[0]["text"]


def test_index_and_timeline(tmp_path):
    pdf = tmp_path / "sumario.pdf"
    _create_pdf(
        pdf,
        [
            "Resolución de inicio 10/03/2025. Funcionario Juan Pérez.",
            "Notificación de cargos 12/03/2025.",
        ],
    )

    pages = extract_text_by_page(pdf)
    index = build_document_index(pdf, pages)
    timeline = build_timeline(pages)

    assert index["tipo_probable"] in {"resolucion", "formulacion_de_cargos", "otro"}
    assert "10/03/2025" in index["fechas_detectadas"]
    assert timeline[0]["fecha"] == "2025-03-10"
    assert timeline[1]["fecha"] == "2025-03-12"
