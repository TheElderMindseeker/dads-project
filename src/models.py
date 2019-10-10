from src.extensions import db


class User(db.Model):
    __tablename__ = "user_accounts"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Length based on the following: http://www.dominicsayers.com/isemail/
    email = db.Column(db.String(255), nullable=False)
    # If I understood correctly, 256 is the commonly used hash result length
    password = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Boolean(), nullable=False, default=False)
