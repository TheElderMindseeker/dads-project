"""Root module with application factory function"""
from flask import Flask
from flask_migrate import Migrate

from livebook.extensions import *
from livebook.models import db
from livebook.views import views


def create_app(config_scheme='debug'):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_pyfile("../config/{}.py".format(config_scheme))
    app.register_blueprint(views)

    db.init_app(app)
    Migrate(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app
