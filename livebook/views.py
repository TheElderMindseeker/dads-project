"""Contains application views"""
from flask import Blueprint, request, render_template
from livebook.models import User

from livebook.extensions import db, bcrypt

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
        # FIXME: generate_password_hash returns bytes which can bring possible hash check problem during login
        new_user = User(email=data['email'], password=bcrypt.generate_password_hash(data['password']), admin=False)
        db.session.add(new_user)
        db.session.commit()
        return "registered"
    return "failed to register"
