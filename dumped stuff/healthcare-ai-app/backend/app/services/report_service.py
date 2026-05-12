import os
import json
from werkzeug.utils import secure_filename
from app.models.report import Report
from app import db

class ReportService:
    def __init__(self):
        self.upload_folder = 'uploads'
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def save_upload(self, file, user_id):
        filename = secure_filename(file.filename)
        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        
        report = Report(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            status='pending'
        )
        
        db.session.add(report)
        db.session.commit()
        
        return report
    
    def get_report(self, report_id, user_id):
        return Report.query.filter_by(id=report_id, user_id=user_id).first()
    
    def get_user_reports(self, user_id):
        return Report.query.filter_by(user_id=user_id).order_by(Report.created_at.desc()).all()
    
    def extract_report_context(self, report):
        if not report or not report.analysis_data:
            return None
        
        analysis = report.get_analysis()
        return {
            'filename': report.filename,
            'upload_date': report.created_at.isoformat(),
            'tests': analysis.get('tests', []) if analysis else [],
            'summary': analysis.get('summary', {}) if analysis else {}
        }
    
    def update_report_analysis(self, report_id, analysis_data):
        report = Report.query.get(report_id)
        if report:
            report.set_analysis(analysis_data)
            report.status = 'completed'
            db.session.commit()
            return report
        return None
    
    def delete_report(self, report_id, user_id):
        report = Report.query.filter_by(id=report_id, user_id=user_id).first()
        if report:
            if os.path.exists(report.file_path):
                os.remove(report.file_path)
            db.session.delete(report)
            db.session.commit()
            return True
        return False