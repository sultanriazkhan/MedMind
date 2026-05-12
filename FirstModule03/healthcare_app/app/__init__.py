"""
Flask Application Factory
Creates and configures the Flask app with all blueprints
"""

from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_object=None):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['REMEMBER_COOKIE_SECURE'] = False
    
    # Initialize extensions with app
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes import (
        auth_bp, home_bp, dashboard_bp, reports_bp,
        lifestyle_bp, ai_chat_bp, blogs_bp, user_bp
    )
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(lifestyle_bp, url_prefix='/lifestyle')
    app.register_blueprint(ai_chat_bp, url_prefix='/ai-chat')
    app.register_blueprint(blogs_bp, url_prefix='/blog')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    # Context processors
    @app.context_processor
    def inject_year():
        """Inject current year into all templates"""
        from datetime import datetime
        return {'current_year': datetime.now().year}
    
    return app


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user from session"""
    # Placeholder - implement with actual database
    from app.models import User
    return User.get_by_id(user_id) if user_id else None