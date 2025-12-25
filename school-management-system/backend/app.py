from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app