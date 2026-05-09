# text_extractor.py
import os
import requests
from flask import Flask, request, render_template, jsonify
import PyPDF2
from docx import Document
import pytesseract
from PIL import Image
import pandas as pd
import chardet

app = Flask(__name__)

# Configuration
ORCHESTRATOR_URL = "http://localhost:5002/process"  # Orchestrator endpoint
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'py', 'xlsx', 'xls'}

# Create upload folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
        return text if text.strip() else None
    except Exception as e:
        return None

def extract_word_text(filepath):
    """Extract text from Word documents (.docx)"""
    try:
        doc = Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        return text if text.strip() else None
    except Exception as e:
        return None

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
        return None

def extract_image_text(filepath):
    """Extract text from images using OCR"""
    try:
        # Open image
        image = Image.open(filepath)
        
        # Preprocess image for better OCR
        if image.mode != 'L':
            image = image.convert('L')
        
        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(image)
        return text if text.strip() else None
    except Exception as e:
        return None

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
        
        return text if text.strip() else None
    except Exception as e:
        return None

def extract_python_text(filepath):
    """Extract text/code from Python files"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ FLASK ROUTES ============

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Main upload page"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'filename' not in request.files:
            return render_template('uploading.html', error='No file uploaded')
        
        file = request.files['filename']
        
        # Check if file is selected
        if not file.filename:
            return render_template('uploading.html', error='No file selected')
        
        # Check file type
        if not allowed_file(file.filename):
            return render_template('uploading.html', 
                                 error=f'File type not supported. Allowed: {", ".join(ALLOWED_EXTENSIONS)}')
        
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Detect file type and extract text
            extracted_text = None
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
            
            # Check if text extraction failed
            if extracted_text is None:
                return render_template('uploading.html',
                                     error=f'Could not extract text from {file_type}. File may be empty or corrupted.')
            
            # Send to orchestrator for processing
            try:
                response = requests.post(
                    ORCHESTRATOR_URL,
                    json={"text": extracted_text},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('success'):
                        # Success - show results
                        return render_template('results.html',
                                             filename=filename,
                                             file_type=file_type,
                                             extracted_text=extracted_text[:1000],  # Preview only
                                             tests=result.get('tests', []),
                                             summary=result.get('summary', {}),
                                             processing_time=result.get('processing_time_ms', 0),
                                             request_id=result.get('request_id', ''))
                    else:
                        # No tests detected
                        return render_template('uploading.html',
                                             filename=filename,
                                             file_type=file_type,
                                             extracted_text=extracted_text[:500],
                                             warning=result.get('error', 'No lab tests detected in this document'),
                                             show_extracted=True)
                else:
                    # Orchestrator error
                    return render_template('uploading.html',
                                         error=f'Orchestrator error: {response.text}',
                                         extracted_text=extracted_text[:500] if extracted_text else None)
                                         
            except requests.exceptions.ConnectionError:
                return render_template('uploading.html',
                                     error='Orchestrator not running. Please start orchestrator.py first (python orchestrator.py)',
                                     extracted_text=extracted_text[:500] if extracted_text else None)
            except requests.exceptions.Timeout:
                return render_template('uploading.html',
                                     error='Processing timeout. The document may be too large or complex.',
                                     extracted_text=extracted_text[:500] if extracted_text else None)
                
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return render_template('uploading.html')

@app.route('/api/extract', methods=['POST'])
def extract_text_api():
    """JSON API endpoint for programmatic access"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400
    
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # Extract text based on file type
    extracted_text = None
    if filename.endswith('.pdf'):
        extracted_text = extract_pdf_text(filepath)
    elif filename.endswith('.docx'):
        extracted_text = extract_word_text(filepath)
    elif filename.endswith('.txt'):
        extracted_text = extract_text_file(filepath)
    elif filename.endswith(('.jpg', '.jpeg', '.png')):
        extracted_text = extract_image_text(filepath)
    else:
        extracted_text = None
    
    os.remove(filepath)
    
    if extracted_text:
        return jsonify({
            "success": True,
            "filename": filename,
            "text": extracted_text,
            "length": len(extracted_text)
        })
    else:
        return jsonify({
            "success": False,
            "error": "Could not extract text from file"
        }), 422

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Check if orchestrator is available
    orchestrator_status = "unknown"
    try:
        response = requests.get("http://localhost:5002/health", timeout=2)
        orchestrator_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        orchestrator_status = "offline"
    
    return jsonify({
        "service": "text-extractor",
        "status": "healthy",
        "orchestrator": orchestrator_status,
        "upload_folder": UPLOAD_FOLDER
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("📄 Text Extractor Service")
    print("="*60)
    print(f"📍 Running on: http://localhost:5000")
    print(f"📍 Orchestrator URL: {ORCHESTRATOR_URL}")
    print(f"📍 Upload folder: {UPLOAD_FOLDER}")
    print("="*60)
    print("\n✅ Make sure orchestrator.py is running on port 5002")
    print("   python orchestrator.py")
    print("\n🌐 Open browser: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)