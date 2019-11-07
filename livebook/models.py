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

    user_infos = db.relationship('UserAdventure', backref=db.backref('user', lazy=False), lazy=True)
    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def is_authenticated(self):
        return True
 

class UserAdventure(db.Model):
    # pylint: disable=missing-function-docstring,no-self-use
    __tablename__ = "user_adventures"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=False)
    adventure = db.Column(db.String(100))
    scene = db.Column(db.String(100), nullable=False)
    stat_infos = db.relationship('AttrInfo', backref=db.backref('user_adventure', lazy=False), lazy=True)


class AttrInfo(db.Model):
    # pylint: disable=missing-function-docstring,no-self-use
    __tablename__ = "attr_info"
    "alias is the name of the attribute from the developer's perspective"
    user_adventure_id = db.Column(db.Integer, db.ForeignKey('user_adventures.id'), nullable=False, primary_key=True)
    alias = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.CheckConstraint(value >= 0, name="value of the attribute must be non-negative"), {})


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
    user_adventure = UserAdventure(user_id=user.id, adventure='link', scene='home')
    db.session.add(user_adventure)
    db.session.commit()
    attr_info = AttrInfo(user_adventure_id=user_adventure.id, alias='strength', value=1010)
    db.session.add(attr_info)
    db.session.commit()

