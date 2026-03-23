import os
from flask import Flask, request, render_template
import PyPDF2
from docx import Document
import pytesseract
from PIL import Image
import pandas as pd
import chardet

app = Flask(__name__)

# ============ TEXT EXTRACTION FUNCTIONS ============

def extract_pdf_text(filepath):
    """Extract text from PDF files"""
    try:
        text = ""
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"--- Page {page_num} ---\n{page_text}\n\n"
        return text if text.strip() else "No text found in PDF"
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

def extract_word_text(filepath):
    """Extract text from Word documents (.docx)"""
    try:
        doc = Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        return text if text.strip() else "No text found in Word document"
    except Exception as e:
        return f"Error extracting Word text: {str(e)}"

def extract_text_file(filepath):
    """Extract text from plain text files"""
    try:
        # Detect encoding
        with open(filepath, 'rb') as file:
            raw_data = file.read()
            detected = chardet.detect(raw_data)
            encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
        
        # Read with detected encoding
        with open(filepath, 'r', encoding=encoding, errors='ignore') as file:
            return file.read()
    except Exception as e:
        return f"Error extracting text file: {str(e)}"

def extract_image_text(filepath):
    """Extract text from images using OCR"""
    try:
        # Open image
        image = Image.open(filepath)
        
        # Optional: Preprocess image for better OCR
        # Convert to grayscale if needed
        if image.mode != 'L':
            image = image.convert('L')
        
        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(image)
        return text if text.strip() else "No text found in image"
    except Exception as e:
        return f"Error extracting image text: {str(e)}"

def extract_excel_text(filepath):
    """Extract text from Excel files"""
    try:
        text = ""
        # Read all sheets
        excel_file = pd.ExcelFile(filepath)
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            text += f"\n=== Sheet: {sheet_name} ===\n"
            text += df.to_string() + "\n"
        
        return text if text.strip() else "No data found in Excel file"
    except Exception as e:
        return f"Error extracting Excel text: {str(e)}"

def extract_python_text(filepath):
    """Extract text/code from Python files"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error extracting Python file: {str(e)}"

# ============ FLASK ROUTE ============

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'filename' not in request.files:
            return render_template('uploading.html', message='No file uploaded')
        
        file = request.files['filename']
        
        # Check if file is selected
        if file.filename == '':
            return render_template('uploading.html', message='No file selected')
        
        filename = file.filename
        
        # Save the file temporarily
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Detect file type and extract text
        extracted_text = ""
        file_type = ""
        
        if filename.endswith('.pdf'):
            file_type = "PDF Document"
            extracted_text = extract_pdf_text(filepath)
            
        elif filename.endswith('.docx'):
            file_type = "Word Document"
            extracted_text = extract_word_text(filepath)
            
        elif filename.endswith('.txt'):
            file_type = "Text File"
            extracted_text = extract_text_file(filepath)
            
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            file_type = "JPEG Image"
            extracted_text = extract_image_text(filepath)
            
        elif filename.endswith('.png'):
            file_type = "PNG Image"
            extracted_text = extract_image_text(filepath)
            
        elif filename.endswith('.py'):
            file_type = "Python File"
            extracted_text = extract_python_text(filepath)
            
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_type = "Excel Spreadsheet"
            extracted_text = extract_excel_text(filepath)
            
        else:
            file_type = "Unknown File Type"
            extracted_text = "File type not supported for text extraction"
        
        return render_template('uploading.html', 
                             filename=filename, 
                             file_type=file_type,
                             extracted_text=extracted_text)
    
    return render_template('uploading.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)