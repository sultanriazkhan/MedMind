from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])
    
    db.init_app(app)
    
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Healthcare AI API is running!',
            'status': 'active',
            'endpoints': {
                'auth': '/api/auth/register, /api/auth/login',
                'reports': '/api/reports/upload, /api/reports/reports',
                'dashboard': '/api/dashboard/stats'
            }
        })
    
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'healthy', 'timestamp': '2024-01-15'})
    
    # Import and register blueprints
    try:
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        print("✅ Auth routes registered")
    except Exception as e:
        print(f"⚠️ Auth routes Error: {e}")
    
    try:
        from app.routes.reports import reports_bp
        app.register_blueprint(reports_bp, url_prefix='/api/reports')
        print("✅ Reports routes registered")
    except Exception as e:
        print(f"⚠️ Reports routes Error: {e}")
    
    try:
        from app.routes.dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
        print("✅ Dashboard routes registered")
    except Exception as e:
        print(f"⚠️ Dashboard routes Error: {e}")
    
    with app.app_context():
        db.create_all()
        print("✅ Database created")
    
    return app