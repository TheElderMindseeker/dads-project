"""Contains application views"""
from flask import Blueprint, request, render_template
from livebook.models import User

from livebook.extensions import db, bcrypt
from flask_login import login_user, current_user

views = Blueprint('views', __name__)  # pylint: disable=invalid-name


@views.route('/')
def hello_world():
    """Outputs hello world greeting to the client"""
    return '<h1>Hello, World!</h1>'


@views.route('/register', methods=['GET', 'POST'])
def register():
    """Serve user registration page"""
    if request.method == 'GET':
        return render_template('register.j2')

    data = request.form
    user_check = User.query.filter_by(email=data['email']).first()
    if user_check is None:
        # pylint: disable=no-member
        new_user = User(email=data['email'],
                        password=bcrypt.generate_password_hash(data['password']).decode(),
                        admin=False)
        db.session.add(new_user)
        db.session.commit()
        return "registered"
    return "failed to register"


@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return "already logged in"

    if request.method == 'GET':
        return render_template('login.j2')

    data = request.form
    user = User.query.filter_by(email=data['email']).first()
    remember = data.get("remember", False) == 'on'
    if user is not None and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user, remember=remember)
        return "logged in"
    return "failed to log in"
