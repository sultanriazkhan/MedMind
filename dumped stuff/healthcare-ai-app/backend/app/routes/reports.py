from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

reports_bp = Blueprint('reports', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@reports_bp.route('/upload', methods=['POST'])
def upload_report():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'report_id': 1,
            'filename': filename
        }), 201
    
    return jsonify({'error': 'File type not allowed'}), 400

@reports_bp.route('/reports', methods=['GET'])
def get_reports():
    return jsonify({
        'reports': [
            {
                'id': 1,
                'filename': 'sample_report.pdf',
                'created_at': '2024-01-15T10:30:00',
                'status': 'completed'
            }
        ]
    })

@reports_bp.route('/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    return jsonify({
        'id': report_id,
        'filename': 'sample_report.pdf',
        'analysis': {
            'tests': [
                {'name': 'Hemoglobin', 'value': '14.2', 'normal_range': '13.5-17.5', 'status': 'normal'},
                {'name': 'White Blood Cells', 'value': '7.5', 'normal_range': '4.5-11.0', 'status': 'normal'},
                {'name': 'Platelets', 'value': '250', 'normal_range': '150-450', 'status': 'normal'}
            ],
            'summary': {
                'total_tests': 3,
                'normal': 3,
                'abnormal': 0,
                'critical': 0
            }
        }
    })

@reports_bp.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    return jsonify({'message': 'Report deleted successfully'})