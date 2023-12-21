"""
Application factory

Initialize application extensions, register blueprints and return the ready application instance
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    config_obj.init_app()

    # TODO: initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # import and register blueprints
    from .main import main
    from .admin import admin
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    return app
