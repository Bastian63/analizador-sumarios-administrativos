# Analizador local de sumarios administrativos (V1)

Aplicación **local y privada** orientada a abogados para organizar expedientes de sumarios administrativos en PDF (incluyendo escaneados).

> ⚖️ **Advertencia jurídica**: esta herramienta es un asistente documental. No determina responsabilidad administrativa ni reemplaza la revisión profesional de un abogado.

## Alcance de la primera versión (MVP)

Prioriza:
1. Carga de PDFs desde carpeta local.
2. Detección de PDFs con/sin texto.
3. OCR local para PDFs escaneados.
4. Extracción de texto por página con referencia a documento/página.
5. Índice documental básico.
6. Cronología preliminar por fechas detectadas.
7. Exportación a Excel (y JSON de respaldo).

## Estructura

- `app/main.py`: interfaz Streamlit.
- `app/ocr.py`: detección y OCR local.
- `app/pdf_reader.py`: extracción por página.
- `app/classifier.py`: índice documental básico.
- `app/timeline.py`: cronología preliminar.
- `app/legal_matrix.py`: placeholder matriz disciplinaria V2.
- `app/exports.py`: exportación Excel/JSON.
- `app/config.py`: configuraciones.
- `tests/test_pipeline.py`: pruebas básicas.
- `scripts/create_fake_data.py`: generación de datos ficticios.

## Instalación

### 1) Requisitos del sistema

- Python 3.11+
- Tesseract OCR instalado localmente (recomendado)
- (Opcional) OCRmyPDF para mejor OCR en PDFs escaneados

En Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-spa ocrmypdf poppler-utils
```

### 2) Dependencias Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

1. Crear datos ficticios (opcional):

```bash
python scripts/create_fake_data.py
```

2. Ejecutar la app:

```bash
streamlit run app/main.py
```

3. En la interfaz, indicar carpeta (por defecto `data/input`) y presionar **Procesar carpeta**.
4. Los resultados se guardan en `data/output/`:
   - `analisis_sumario_YYYYMMDD_HHMMSS.xlsx`
   - `analisis_sumario_YYYYMMDD_HHMMSS.json`

## Datos de prueba ficticios

El script `scripts/create_fake_data.py` genera:
- `data/input/ejemplo_sumario/01_resolucion_inicio.pdf` (texto nativo)
- `data/input/ejemplo_sumario/02_declaracion_scan.pdf` (imagen simulando escaneo)

## Pruebas básicas

```bash
pytest -q
```

## Limitaciones actuales

- Clasificación documental simple por palabras clave.
- Detección de personas basada en regex (puede tener falsos positivos/negativos).
- Cronología basada solo en fechas detectadas en texto.
- No implementa aún matriz disciplinaria avanzada ni alertas jurídicas exhaustivas.
- Calidad OCR depende de calidad del escaneo e instalación local.

## Mejoras sugeridas para V2

1. Matriz disciplinaria completa y alertas jurídicas configurables.
2. Persistencia en SQLite para expedientes grandes.
3. Mejor NER para personas/cargos con modelos NLP en español.
4. Reglas jurídicas trazables por tipo de riesgo (siempre como alerta revisable).
5. Exportación Word (`python-docx`) con citas automáticas documento/página.
6. Gestión multi-expediente y filtros avanzados en UI.
