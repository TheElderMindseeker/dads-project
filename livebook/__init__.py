"""Root module with application factory function"""
from flask import Flask

from livebook.extensions import *
from livebook.views import views


def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_pyfile("../config/debug.py")
    app.register_blueprint(views)

    db.init_app(app)
    bcrypt.init_app(app)

    return app
