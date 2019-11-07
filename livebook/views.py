"""Contains application views"""
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required

from livebook.extensions import bcrypt
from livebook.models import User, db, UserAdventure, AttrInfo

views = Blueprint('views', __name__)  # pylint: disable=invalid-name


@views.route('/')
def hello_world():
    """Outputs hello world greeting to the client"""
    return '<h1>Hello, World!</h1>'


@views.route('/register', methods=['GET', 'POST'])
def register():
    """Serve user registration page and process register form"""
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
    """Serve user login page and process login form"""
    if current_user is not None and current_user.is_authenticated:
        return "already logged in"

    if request.method == 'GET':
        return render_template('login.j2', next=request.args.get('next'))

    data = request.form
    user = User.query.filter_by(email=data['email']).first()
    remember = data.get("remember", False) == 'on'
    if user is not None and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user, remember=remember)
        next_page = data.get('next')
        if next_page is not None:
            return redirect(next_page)
        return "logged in"
    return "failed to log in"


@views.route('/page', methods=['GET'])
@login_required
def show_adventure():
    return render_template("book_page.j2")


@views.route('/attribute', methods=['GET', 'POST'])
def attribute():
    data = request.json
    user_adventure = UserAdventure.query.filter_by(
        user_id=data['user_id'], adventure=data['adventure']).first_or_404(description='no such user or adventure')
    attr_info = AttrInfo.query.filter_by(
        user_adventure_id=user_adventure.id,
        alias=data['alias']).first_or_404(description='no such user, adventure or attribute')
    if request.method == 'GET':
        return f'<h1>The value of {data["alias"]} is {attr_info.value}</h1>'

    attr_info.value = data['value']
    db.session.commit()
    return "successfully changed the attr"


@views.route('/scene', methods=['GET', 'POST'])
def scene():
    data = request.json
    user_adventure = UserAdventure.query.filter_by(
        user_id=data['user_id'], adventure=data['adventure']).first_or_404(description='no such user or adventure')
    if request.method == 'GET':
        return f'<h1>The scene is {user_adventure.scene}</h1>'

    user_adventure.scene = data['scene']
    db.session.commit()
    return "successfully changed the scene"
