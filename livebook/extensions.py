from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from livebook.models import User

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "views.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(email=user_id).first()
