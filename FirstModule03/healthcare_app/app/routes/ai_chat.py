# app/routes/ai_chat.py
"""AI Chat Routes
Health AI chat interfaces
"""

from flask import Blueprint, render_template
from flask_login import login_required

ai_chat_bp = Blueprint('ai_chat', __name__)


@ai_chat_bp.route('/health-chat')
@login_required
def health_chat():
    """General health AI chat interface"""
    return render_template('ai_chat/health_chat.html', page_title='AI Health Assistant')


@ai_chat_bp.route('/report-aware')
@login_required
def report_aware_chat():
    """Report-aware AI chat interface"""
    return render_template('ai_chat/report_aware_chat.html', page_title='Report-Aware AI Chat')