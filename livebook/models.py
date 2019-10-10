"""Database models for the application"""
# pylint: disable=no-member,too-few-public-methods
from livebook.extensions import db


class User(db.Model):
    """User account in the application"""
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
        # TODO: Figure a good way to deal with this part
        return True
