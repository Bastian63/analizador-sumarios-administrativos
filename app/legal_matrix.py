from __future__ import annotations


def build_minimal_legal_matrix(page_rows: list[dict]) -> list[dict]:
    """Placeholder para V1: devuelve matriz mínima vacía sin conclusiones automáticas."""
    return [
        {
            "hecho_o_cargo_posible": "Revisión manual requerida",
            "documento_fuente": row["file_name"],
            "pagina": row["page"],
            "prueba_asociada": (row["text"] or "")[:200],
            "descargo_o_defensa_detectada": "Pendiente análisis profesional",
            "contradicciones_detectadas": "No evaluado automáticamente",
            "omisiones_procedimentales_posibles": "No evaluado automáticamente",
            "riesgo_juridico": "Revisar coherencia entre cargos, prueba y motivación",
            "conclusion_preliminar": "Sin conclusión automática",
            "nivel_confianza": "bajo",
        }
        for row in page_rows[:20]
    ]
