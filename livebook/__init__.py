"""Root module with application factory function"""
from flask import Flask
from flask_migrate import Migrate

from livebook.extensions import *
from livebook.models import db, init_db
from livebook.views import views


def create_app(config_scheme='debug'):
    """Application factory function"""
    # App creation
    app = Flask(__name__)
    app.config.from_pyfile("../config/{}.py".format(config_scheme))
    app.register_blueprint(views)

    # Extensions initialization
    db.init_app(app)
    migration.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Additional processing
    app.cli.add_command(init_db)

    return app
