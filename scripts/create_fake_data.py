from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "data" / "input" / "ejemplo_sumario"


def _make_simple_pdf(path: Path, lines: list[str]) -> None:
    """Genera un PDF mínimo con texto, sin dependencias externas."""
    commands = ["BT /F1 12 Tf 72 770 Td"]
    first = True
    for line in lines:
        safe = line.replace("(", r"\(").replace(")", r"\)")
        if not first:
            commands.append("0 -16 Td")
        commands.append(f"({safe}) Tj")
        first = False
    commands.append("ET")
    content = "\n".join(commands).encode("latin-1", "replace")

    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        (
            b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
        ),
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
        f"5 0 obj << /Length {len(content)} >> stream\n".encode()
        + content
        + b"\nendstream endobj\n",
    ]

    pdf = b"%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf += obj

    xref_pos = len(pdf)
    pdf += f"xref\n0 {len(objects)+1}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n".encode()
    pdf += (
        f"trailer << /Root 1 0 R /Size {len(objects)+1} >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n"
    ).encode()

    path.write_bytes(pdf)


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    _make_simple_pdf(
        OUT / "01_resolucion_inicio.pdf",
        [
            "RESOLUCION EXENTA N 123",
            "Fecha: 10/03/2025",
            "Se inicia sumario administrativo por hechos del 05/03/2025.",
            "Funcionario involucrado: Juan Perez.",
            "Se notifica formulacion de cargos el 12/03/2025.",
        ],
    )

    _make_simple_pdf(
        OUT / "02_declaracion_scan.pdf",
        [
            "ACTA DE DECLARACION (simulada)",
            "Fecha: 14/03/2025",
            "Declara Maria Soto sobre los hechos investigados.",
            "Se acompana prueba documental.",
        ],
    )

    print(f"Datos ficticios creados en: {OUT}")


if __name__ == "__main__":
    main()
