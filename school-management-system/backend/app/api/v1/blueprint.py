from flask import Blueprint

from app.modules.users.routes import users_bp
from app.modules.academics.routes import academics_bp
from app.modules.finance.routes import finance_bp
from app.modules.admin.routes import admin_bp


api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api_v1_bp.register_blueprint(users_bp, url_prefix='/users')
api_v1_bp.register_blueprint(academics_bp, url_prefix='/academics')
api_v1_bp.register_blueprint(finance_bp, url_prefix='/finance')
api_v1_bp.register_blueprint(admin_bp, url_prefix='/admin')


