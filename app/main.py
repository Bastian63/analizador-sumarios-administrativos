from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from .classifier import build_document_index
from .config import INPUT_DIR, OUTPUT_DIR
from .exports import export_excel, export_json
from .ocr import apply_ocr, pdf_has_text
from .pdf_reader import extract_text_by_page
from .timeline import build_timeline

st.set_page_config(page_title="Analizador de Sumarios", layout="wide")

st.title("Analizador local de sumarios administrativos")
st.caption(
    "Asistente documental para abogados. No reemplaza criterio jurídico profesional "
    "ni determina responsabilidad administrativa."
)

folder_str = st.text_input("Carpeta de PDFs", value=str(INPUT_DIR))
process_btn = st.button("Procesar carpeta")

if process_btn:
    folder = Path(folder_str)
    if not folder.exists():
        st.error("La carpeta indicada no existe.")
        st.stop()

    pdf_files = sorted(folder.glob("*.pdf"))
    if not pdf_files:
        st.warning("No se encontraron PDFs en la carpeta.")
        st.stop()

    all_pages = []
    index_rows = []

    with st.spinner("Analizando documentos..."):
        for pdf_path in pdf_files:
            source = pdf_path
            needs_ocr = not pdf_has_text(pdf_path)
            if needs_ocr:
                st.info(f"Aplicando OCR local a: {pdf_path.name}")
                source = apply_ocr(pdf_path, OUTPUT_DIR / "ocr")

            pages = extract_text_by_page(source)
            for p in pages:
                p["source_original"] = pdf_path.name
            all_pages.extend(pages)
            index_rows.append(build_document_index(pdf_path, pages))

    timeline_rows = build_timeline(all_pages)

    st.subheader("Índice documental")
    st.dataframe(pd.DataFrame(index_rows), use_container_width=True)

    st.subheader("Cronología preliminar")
    st.dataframe(pd.DataFrame(timeline_rows), use_container_width=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_path = OUTPUT_DIR / f"analisis_sumario_{stamp}.xlsx"
    json_path = OUTPUT_DIR / f"analisis_sumario_{stamp}.json"
    export_excel(index_rows, timeline_rows, excel_path)
    export_json(
        {"indice_documental": index_rows, "cronologia": timeline_rows, "paginas": all_pages},
        json_path,
    )

    st.success("Proceso finalizado.")
    st.write(f"Excel generado: `{excel_path}`")
    st.write(f"JSON generado: `{json_path}`")

st.divider()
st.markdown(
    """
### Resumen jurídico preliminar
- Resultado orientado a **apoyo documental**.
- Cada hallazgo debe verificarse en documento y página fuente.
- No emite sanciones ni conclusiones definitivas.
"""
)
