from .chips import chips_bp
from .aparelhos import aparelhos_bp
from .recargas import recargas_bp
from .relacionamentos import relacionamentos_bp
from .dashboard import dashboard_bp
from .admin import admin_bp
from .admin_empresa import admin_empresa_bp
from .auth import auth_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(chips_bp)
    app.register_blueprint(aparelhos_bp)
    app.register_blueprint(recargas_bp)
    app.register_blueprint(relacionamentos_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_empresa_bp)
