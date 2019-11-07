"""Contains application views"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_user

from livebook.extensions import bcrypt
from livebook.models import User, db
from livebook.parsers.google_sheets.parser import read_stats, read_initial_scenes, get_scene_names, read_scene

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
                        password=bcrypt.generate_password_hash(
                            data['password']).decode(),
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
        return render_template('login.j2')

    data = request.form
    user = User.query.filter_by(email=data['email']).first()
    remember = data.get("remember", False) == 'on'
    if user is not None and bcrypt.check_password_hash(user.password,
                                                       data['password']):
        login_user(user, remember=remember)
        return "logged in"
    return "failed to log in"


@views.route('/player', methods=['GET'])
def get_player():
    """Serve user login page and process login form"""
    out = {}
    if current_user is not None and current_user.is_authenticated:
        out['id'] = current_user.id
        # TODO: Add other fields for the player
    return jsonify(out)


@views.route('/adventure', methods=['GET'])
def get_adventure():
    out = {'stats': [i.__dict__ for i in read_stats()], 'scene_names': get_scene_names()}

    start, ends = read_initial_scenes()

    out['start_scene'] = start
    out['end_scenes'] = ends
    return jsonify(out)


@views.route('/adventure/scene/<scene>', methods=['GET'])
def get_scene(scene):
    out = {}
    if scene in get_scene_names():
        scene_info = read_scene(scene)
        scene_info.parse_text(read_stats())
        out['description'] = scene_info.text
        out['options'] = [i.__dict__ for i in scene_info.options]
    return jsonify(out)
