from flask import Flask
from .config import Config
from app.extensions import db, migrate   # ✅ SINGLE SOURCE OF TRUTH
from app.middleware.auth_context import load_user_context
from app.core.audit_events import register_audit_events
from app.core.error_handlers import register_error_handlers
from app.api.v1.blueprint import api_v1_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1️⃣ Init DB
    db.init_app(app)

    # 2️⃣ Import ALL models (CRITICAL)
    with app.app_context():
        from app.models import base, users, academics, finance

        # 3️⃣ Register audit hooks AFTER models are loaded
        register_audit_events()

    # 4️⃣ Init migrations AFTER models
    migrate.init_app(app, db)

    # 5️⃣ Register blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_v1_bp)
    register_error_handlers(app)

    # 6️⃣ Load user context before every request
    @app.before_request
    def before_request():
        load_user_context()

    return app
