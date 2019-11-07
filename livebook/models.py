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

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def is_authenticated(self):
        return True


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

