import os
from flask import Flask, request, render_template
app= Flask(__name__)
@app.route('/', methods=['GET', 'POST'  ])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return render_template('uploading.html', message='No file selected')
        filename = file.filename
        if filename.endswith('.pdf'):
            file_type = "PDF Document"
        elif filename.endswith('.docx'):
            file_type = "Word Document"
        elif filename.endswith('.txt'):
            file_type = "Text File"
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            file_type = "JPEG Image"
        elif filename.endswith('.png'):
            file_type = "PNG Image"
        elif filename.endswith('.py'):
            file_type = "Python File"
        else:
            file_type = "Unknown File Type"
        return render_template('uploading.html', filename=filename, file_type=file_type)
    return render_template('uploading.html')
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)