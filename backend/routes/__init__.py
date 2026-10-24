"""路由注册"""
from .audio import bp as audio_bp
from .guide import bp as guide_bp
from .home import bp as home_bp
from .map import bp as map_bp
from .plan import bp as plan_bp


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(guide_bp)
    app.register_blueprint(audio_bp)
