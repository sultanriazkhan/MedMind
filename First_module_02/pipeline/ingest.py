"""
STEP 1 & 2: Ingestion Layer + OCR
Handles all input types: images, PDF, DOCX, TXT, pasted text
"""
import io
from typing import Union, Optional
from fastapi import HTTPException
import numpy as np
from PIL import Image

# Lazy load heavy dependencies
_reader = None

def get_ocr_reader():
    global _reader
    if _reader is None:
        try:
            import easyocr
            _reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        except ImportError:
            raise HTTPException(status_code=500, detail="OCR library not available")
    return _reader

def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from image using EasyOCR"""
    try:
        reader = get_ocr_reader()
        image = Image.open(io.BytesIO(file_bytes))
        image_np = np.array(image)
        results = reader.readtext(image_np, detail=0)
        return " ".join(results)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OCR failed: {str(e)}")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using PyMuPDF"""
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF parsing failed: {str(e)}")

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX using python-docx"""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DOCX parsing failed: {str(e)}")

def process_uploaded_file(file_content: bytes, content_type: str) -> tuple[str, str]:
    """
    Process uploaded file based on MIME type
    
    Returns:
        tuple: (source_type, extracted_text)
    """
    if content_type.startswith('image/'):
        return "image", extract_text_from_image(file_content)
    elif content_type == 'application/pdf':
        return "pdf", extract_text_from_pdf(file_content)
    elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return "docx", extract_text_from_docx(file_content)
    elif content_type == 'text/plain':
        return "text", file_content.decode('utf-8')
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {content_type}")

def process_text_input(text: str) -> tuple[str, str]:
    """Process pasted text input"""
    return "pasted_text", text