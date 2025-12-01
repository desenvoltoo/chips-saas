from .auth import auth_bp
from .dashboard import bp_dashboard
from .chips import chips_bp
from .aparelhos import aparelhos_bp
from .recargas import recargas_bp
from .relacionamentos import relacionamentos_bp
from .admin import admin_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(bp_dashboard)
    app.register_blueprint(chips_bp)
    app.register_blueprint(aparelhos_bp)
    app.register_blueprint(recargas_bp)
    app.register_blueprint(relacionamentos_bp)
    app.register_blueprint(admin_bp)
