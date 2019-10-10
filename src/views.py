"""Contains application views"""
from flask import Blueprint, request, render_template, flash
from src.models import User

from src.extensions import db, bcrypt

views = Blueprint('views', __name__)  # pylint: disable=invalid-name


@views.route('/')
def hello_world():
    """Outputs hello world greeting to the client"""
    return '<h1>Hello, World!</h1>'


@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.j2')
    elif request.method == 'POST':
        data = request.form
        user_check = User.query.filter_by(email=data['email']).first()
        if user_check is None:
            new_user = User(email=data['email'], password=bcrypt.generate_password_hash(data['password']), admin=False)
            db.session.add(new_user)
            db.session.commit()
            return "registered"
        return "failed to register"
