"""Database models for the application"""
# pylint: disable=no-member,too-few-public-methods
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import create_database, database_exists

db = SQLAlchemy()  # pylint: disable=invalid-name


class User(db.Model):
    """User account in the application"""
    # pylint: disable=missing-function-docstring,no-self-use
    __tablename__ = "user_accounts"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Length based on the following: http://www.dominicsayers.com/isemail/
    email = db.Column(db.String(255), nullable=False)
    # If I understood correctly, 256 is the commonly used hash result length
    password = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Boolean(), nullable=False, default=False)

    attributes = db.relationship('GameInfo', backref=db.backref('user', lazy=False), lazy=True)

    scenes = db.relationship('SceneInfo', backref=db.backref('user', lazy=False), lazy=True)
    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def is_authenticated(self):
        return True


class GameInfo(db.Model):
    # pylint: disable=missing-function-docstring,no-self-use
    __tablename__ = "game_info"
    user_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=False, primary_key=True)
    adventure = db.Column(db.String(100), primary_key=True)
    "alias is the name of the attribute from the developer's perspective"
    alias = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.CheckConstraint(value >= 0, name="value of the attribute must be non-negative"), {})


class SceneInfo(db.Model):
    # pylint: disable=missing-function-docstring,no-self-use
    user_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=False, primary_key=True)
    adventure = db.Column(db.String(100), primary_key=True)
    scene = db.Column(db.String(100), nullable=False)



@click.command('init-db')
@with_appcontext
def init_db():
    """
    Creates the database (if needed) and re-creates the tables.
    Use with "flask init-db".
    """
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
    db.drop_all()
    db.create_all()


@click.command('gen-data')
@with_appcontext
def gen_data():
    user = User(email='johny',
            password='passwd',
            admin=False)
    db.session.add(user)
    db.session.commit()
    game_info = GameInfo(user_id=user.id, adventure='link', alias='strength', value=11)
    db.session.add(game_info)
    db.session.commit()
    scene_info = SceneInfo(user_id=user.id, adventure='link', scene='home')
    db.session.add(scene_info)
    db.session.commit()

