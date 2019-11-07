"""Contains objects representing Flask extensions"""
# pylint: disable=invalid-name
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from livebook.models import User

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "views.login"
migration = Migrate()


@login_manager.user_loader
def load_user(user_id):
    """Load user object from database"""
    return User.query.filter_by(email=user_id).first()
