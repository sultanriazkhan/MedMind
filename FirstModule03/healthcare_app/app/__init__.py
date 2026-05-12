# app/__init__.py
from flask import Flask
from flask_login import LoginManager
import os

# Initialize Login Manager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # CRITICAL: Secret key MUST be set for session to work
    app.config['SECRET_KEY'] = 'your-very-secret-key-change-this-in-production-2024'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['REMEMBER_COOKIE_DURATION'] = 30 * 24 * 3600  # 30 days
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    
    # Import User model
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from session - THIS IS CRITICAL"""
        print(f"Loading user with ID: {user_id}")  # Debug
        if user_id:
            user = User.get_by_id(user_id)
            print(f"User loaded: {user}")  # Debug
            return user
        return None
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.home import home_bp
    from app.routes.reports import reports_bp
    from app.routes.lifestyle import lifestyle_bp
    from app.routes.ai_chat import ai_chat_bp
    from app.routes.blogs import blogs_bp
    from app.routes.user import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(home_bp)
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(lifestyle_bp, url_prefix='/lifestyle')
    app.register_blueprint(ai_chat_bp, url_prefix='/ai-chat')
    app.register_blueprint(blogs_bp, url_prefix='/blog')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    @app.context_processor
    def inject_year():
        from datetime import datetime
        return {'current_year': datetime.now().year}
    
    return app