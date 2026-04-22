from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def export_excel(index_rows: list[dict], timeline_rows: list[dict], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame(index_rows).to_excel(writer, sheet_name="indice_documental", index=False)
        pd.DataFrame(timeline_rows).to_excel(writer, sheet_name="cronologia", index=False)
    return output_path


def export_json(payload: dict, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return output_path
