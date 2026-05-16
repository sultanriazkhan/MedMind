from flask import Flask, request, render_template_string, redirect, url_for, flash
import os
from pathlib import Path
import shutil

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx', 'txt', 'xlsx'}

# Create upload folder if it doesn't exist
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    """Get readable file type from extension"""
    types = {
        'pdf': 'PDF Document',
        'png': 'PNG Image',
        'jpg': 'JPEG Image',
        'jpeg': 'JPEG Image',
        'docx': 'Word Document',
        'txt': 'Text File',
        'xlsx': 'Excel Spreadsheet'
    }
    ext = filename.rsplit('.', 1)[1].lower()
    return types.get(ext, 'Unknown')

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>File Upload - Document Ingestion</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 50px auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        
        .upload-form {
            margin: 20px 0;
        }
        
        .file-input-group {
            margin-bottom: 20px;
        }
        
        .file-input-group label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: bold;
        }
        
        input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px dashed #ddd;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        input[type="file"]:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #5a67d8;
        }
        
        .flash-messages {
            margin: 20px 0;
            padding: 15px;
            border-radius: 8px;
        }
        
        .flash-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .flash-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .uploaded-files {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
        
        .uploaded-files h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .file-list {
            list-style: none;
        }
        
        .file-item {
            background: #f8f9fa;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .file-info {
            flex: 1;
        }
        
        .file-name {
            font-weight: bold;
            color: #333;
        }
        
        .file-type {
            font-size: 12px;
            color: #667eea;
            margin-left: 10px;
        }
        
        .file-size {
            font-size: 12px;
            color: #666;
            margin-left: 10px;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            background: #667eea;
            color: white;
            border-radius: 4px;
            font-size: 11px;
        }
        
        .supported-formats {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 14px;
            color: #666;
            text-align: center;
        }
        
        .supported-formats span {
            display: inline-block;
            background: white;
            padding: 4px 8px;
            margin: 0 4px;
            border-radius: 4px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📄 Document Ingestion Platform</h1>
        <div class="subtitle">Upload your documents for processing</div>
        
        <!-- Upload Form -->
        <form method="POST" action="/upload" enctype="multipart/form-data" class="upload-form">
            <div class="file-input-group">
                <label for="file">Select Document:</label>
                <input type="file" name="file" id="file" accept=".pdf,.png,.jpg,.jpeg,.docx,.txt,.xlsx" required>
            </div>
            <button type="submit">Upload Document</button>
        </form>
        
        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash-messages flash-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <!-- List Uploaded Files -->
        {% if files %}
        <div class="uploaded-files">
            <h3>📁 Uploaded Documents ({{ files|length }})</h3>
            <ul class="file-list">
                {% for file in files %}
                <li class="file-item">
                    <div class="file-info">
                        <span class="file-name">{{ file.filename }}</span>
                        <span class="file-type">{{ file.type }}</span>
                        <span class="file-size">({{ file.size_kb }} KB)</span>
                    </div>
                    <span class="badge">{{ file.extension }}</span>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        <div class="supported-formats">
            📌 Supported formats: 
            <span>.PDF</span> <span>.DOCX</span> <span>.TXT</span>
            <span>.PNG</span> <span>.JPG</span> <span>.XLSX</span>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Display upload page with list of uploaded files"""
    files = []
    
    # Get list of uploaded files
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
                size_bytes = os.path.getsize(filepath)
                size_kb = round(size_bytes / 1024, 2)
                
                files.append({
                    'filename': filename,
                    'type': get_file_type(filename),
                    'extension': extension.upper(),
                    'size_kb': size_kb,
                    'size_bytes': size_bytes
                })
        
        # Sort by upload time (newest first)
        files.sort(key=lambda x: os.path.getctime(os.path.join(UPLOAD_FOLDER, x['filename'])), reverse=True)
    
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    
    # Check if file is present
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Check if file type is allowed
    if not allowed_file(file.filename):
        extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'unknown'
        flash(f'File type .{extension} is not supported. Allowed: PDF, PNG, JPG, DOCX, TXT, XLSX', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get file extension and type
        extension = file.filename.rsplit('.', 1)[1].lower()
        file_type = get_file_type(file.filename)
        
        # Save file with original name
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Handle duplicate filenames
        counter = 1
        while os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        
        # Save the file
        file.save(filepath)
        
        # Get file size
        file_size = os.path.getsize(filepath)
        size_kb = round(file_size / 1024, 2)
        
        # Success message
        flash(f'✅ {filename} ({file_type}, {size_kb} KB) uploaded successfully!', 'success')
        
    except Exception as e:
        flash(f'Error uploading file: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)