"""Root module with application factory function"""
from flask import Flask

from src.views import views


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_pyfile("../config/debug.py")
    app.register_blueprint(views)
    return app
