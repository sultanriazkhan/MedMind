from flask import Blueprint, request, jsonify, Response, stream_with_context
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ai_service import AIService
from app.services.report_service import ReportService
import json

chat_bp = Blueprint('chat', __name__)
ai_service = AIService()
report_service = ReportService()

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    data = request.json
    message = data.get('message')
    report_context = data.get('report_context')
    report_id = data.get('report_id')
    
    def generate():
        if report_context and report_id:
            report = report_service.get_report(report_id, user_id)
            context_data = report_service.extract_report_context(report)
            yield from ai_service.stream_chat_with_context(message, context_data, user_id)
        else:
            yield from ai_service.stream_chat(message, user_id)
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@chat_bp.route('/chat/suggestions', methods=['GET'])
@jwt_required()
def get_suggestions():
    user_id = get_jwt_identity()
    suggestions = ai_service.get_suggested_prompts(user_id)
    return jsonify({'suggestions': suggestions})

@chat_bp.route('/chat/clear', methods=['POST'])
@jwt_required()
def clear_chat():
    user_id = get_jwt_identity()
    ai_service.clear_conversation(user_id)
    return jsonify({'message': 'Conversation cleared'})