from app import db
from datetime import datetime
import json

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')
    analysis_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_analysis(self, data):
        self.analysis_data = json.dumps(data)
        self.status = 'completed'
    
    def get_analysis(self):
        return json.loads(self.analysis_data) if self.analysis_data else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'file_size': self.file_size,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'analysis': self.get_analysis()
        }