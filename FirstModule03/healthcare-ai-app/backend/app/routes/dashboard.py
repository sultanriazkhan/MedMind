from flask import Blueprint, jsonify

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'total_reports': 12,
        'abnormal_findings': 3,
        'ai_sessions': 45,
        'health_score': 85,
        'recent_activity': [
            {'type': 'report', 'title': 'Blood Test Results', 'date': '2024-01-15'},
            {'type': 'chat', 'title': 'AI Consultation', 'date': '2024-01-14'},
            {'type': 'recommendation', 'title': 'Diet Plan Generated', 'date': '2024-01-13'}
        ]
    })