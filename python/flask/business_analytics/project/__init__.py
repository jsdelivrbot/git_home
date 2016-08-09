from flask import Flask, current_app
from .auth import auth as auth_blueprint
from .dashboard import dashboard as dashboard_blueprint
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    return app
