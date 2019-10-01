"""Contains application views"""
from flask import Blueprint, request, render_template

from src.extensions import bcrypt

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
        print("POST")
        print(request.form)
        return "NO"
