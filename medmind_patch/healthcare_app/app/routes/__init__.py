from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "medmind-dev-secret-key-change-in-production"

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to access this page."
    login_manager.login_message_category = "warning"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    from app.routes.auth import auth_bp
    from app.routes.home import home_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.reports import reports_bp
    from app.routes.lifestyle import lifestyle_bp
    from app.routes.ai_chat import ai_chat_bp
    from app.routes.blogs import blogs_bp
    from app.routes.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(lifestyle_bp)
    app.register_blueprint(ai_chat_bp)
    app.register_blueprint(blogs_bp)
    app.register_blueprint(user_bp)

    return app