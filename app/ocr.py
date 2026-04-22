from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import fitz
import pytesseract
from pdf2image import convert_from_path


def pdf_has_text(pdf_path: Path, min_chars: int = 30) -> bool:
    """Retorna True si el PDF ya contiene texto extraíble."""
    doc = fitz.open(pdf_path)
    try:
        total = 0
        for page in doc:
            total += len(page.get_text().strip())
            if total >= min_chars:
                return True
        return False
    finally:
        doc.close()


def apply_ocr(pdf_path: Path, output_dir: Path) -> Path:
    """Aplica OCR local y retorna la ruta del PDF resultante."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = output_dir / f"{pdf_path.stem}_ocr.pdf"

    if shutil.which("ocrmypdf"):
        cmd = [
            "ocrmypdf",
            "--force-ocr",
            "--skip-text",
            str(pdf_path),
            str(output_pdf),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_pdf

    # Fallback local con Tesseract + pdf2image
    images = convert_from_path(str(pdf_path), dpi=200)
    text_pages = [pytesseract.image_to_string(img, lang="spa") for img in images]
    doc = fitz.open()
    for text in text_pages:
        page = doc.new_page()
        page.insert_text((72, 72), text or "[OCR sin texto legible]")
    doc.save(output_pdf)
    doc.close()
    return output_pdf
