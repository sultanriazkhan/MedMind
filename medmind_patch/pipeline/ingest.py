"""
pipeline/ingest.py
Ingestion layer: returns clean raw text only.
"""
import io
from fastapi import HTTPException


def _ocr_image_bytes(image_bytes: bytes) -> str:
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(io.BytesIO(image_bytes))
        return pytesseract.image_to_string(img)
    except ImportError:
        pass
    try:
        import easyocr
        import numpy as np
        from PIL import Image
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        img = Image.open(io.BytesIO(image_bytes))
        results = reader.readtext(np.array(img), detail=0)
        return " ".join(results)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OCR failed: {e}")


def _extract_pdf(file_bytes: bytes) -> str:
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages = [page.get_text() for page in doc]
        doc.close()
        text = "\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass
    # Fallback: render first page and OCR
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page = doc[0]
        pix = page.get_pixmap(dpi=200)
        doc.close()
        return _ocr_image_bytes(pix.tobytes("png"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF extraction failed: {e}")


def _extract_docx(file_bytes: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DOCX parsing failed: {e}")


def process_uploaded_file(file_content: bytes, content_type: str) -> tuple:
    ct = (content_type or "").lower()
    if ct.startswith("image/"):
        return "image", _ocr_image_bytes(file_content)
    if ct == "application/pdf":
        return "pdf", _extract_pdf(file_content)
    if "wordprocessingml" in ct or ct == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return "docx", _extract_docx(file_content)
    if ct in ("text/plain", "text/csv") or ct.startswith("text/"):
        return "text", file_content.decode("utf-8", errors="replace")
    raise HTTPException(status_code=400, detail=f"Unsupported file type: {content_type}")


def process_text_input(text: str) -> tuple:
    return "pasted_text", text