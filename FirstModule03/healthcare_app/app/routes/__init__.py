"""
Routes Blueprints Initialization
Imports all route blueprints for registration
"""

from .auth import auth_bp
from .home import home_bp
from .dashboard import dashboard_bp
from .reports import reports_bp
from .lifestyle import lifestyle_bp
from .ai_chat import ai_chat_bp
from .blogs import blogs_bp
from .user import user_bp

__all__ = [
    'auth_bp',
    'home_bp', 
    'dashboard_bp',
    'reports_bp',
    'lifestyle_bp',
    'ai_chat_bp',
    'blogs_bp',
    'user_bp'
]