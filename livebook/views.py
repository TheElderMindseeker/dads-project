"""Contains application views"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_user, login_required

from livebook.extensions import bcrypt
from livebook.models import User, db, UserAdventure, AttrInfo
from livebook.parsers.google_sheets.parser import read_stats, read_initial_scenes, get_scene_names, read_scene, \
    spreadsheet_id

views = Blueprint('views', __name__)  # pylint: disable=invalid-name

# TODO: this method has its flaws, should probably redo tho make it better
#  At least we got some caching?
stats = read_stats()
start_scene, end_scenes = read_initial_scenes()
scene_names = get_scene_names()


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

        # TODO: currently we only support one adventure and create the base at registration.
        #  Probably better redo this part
        new_adventure = UserAdventure(user=new_user, adventure=spreadsheet_id, scene=start_scene)
        db.session.add(new_adventure)
        db.session.commit()

        for stat in stats:
            new_stat = AttrInfo(user_adventure_id=new_adventure.id, alias=stat.alias, value=stat.default_value)
            db.session.add(new_stat)

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


@views.route('/player', methods=['GET'])
def get_player():
    """Serve user login page and process login form"""
    out = {}
    if current_user is not None and current_user.is_authenticated:
        user_adventure = UserAdventure.query.filter_by(user_id=current_user.id).first()
        user_stats = AttrInfo.query.filter_by(user_adventure_id=user_adventure.id).all()

        out['id'] = current_user.id
        out['current_scene'] = user_adventure.scene
        out['current_stats'] = dict()
        for stat in user_stats:
            out['current_stats'][stat.alias] = stat.value

    return jsonify(out)


@views.route('/adventure', methods=['GET'])
def get_adventure():
    out = {
        'stats': [i.__dict__ for i in stats],
        'scene_names': scene_names,
        'start_scene': start_scene,
        'end_scenes': end_scenes
    }

    return jsonify(out)


# Utility function to get a scene from the adventure
def get_scene(scene):
    out = {}
    if scene in scene_names:
        scene_info = read_scene(scene)
        scene_info.parse_text(stats)
        out['description'] = scene_info.text
        out['options'] = [i.__dict__ for i in scene_info.options]
    return out


@views.route('/adventure/next/<int:index>', methods=['GET'])
def next_scene(index):
    out = {}
    if current_user is not None and current_user.is_authenticated:
        user_adventure = UserAdventure.query.filter_by(user_id=current_user.id).first()
        scene = get_scene(user_adventure.scene)
        out = get_scene(scene['options'][index]['next'])
        out['description'] = scene['options'][index]['prompt'] + '\n' + out['description']

        user_adventure.scene = scene['options'][index]['next']
        db.session.commit()
    return jsonify(out)


@views.route('/adventure/scene/<string:scene>', methods=['GET'])
def return_scene(scene):
    return jsonify(get_scene(scene))


@views.route('/increase/<string:alias>', methods=['POST'])
def increase_stat(alias):
    if current_user is not None and current_user.is_authenticated:
        user_adventure = UserAdventure.query.filter_by(user_id=current_user.id).first()
        stat = AttrInfo.query.filter_by(user_adventure_id=user_adventure.id, alias=alias).first()
        stat.value += 1
        db.session.commit()
    return jsonify({}), 200


@views.route('/decrease/<string:alias>', methods=['POST'])
def decrease_stat(alias):
    if current_user is not None and current_user.is_authenticated:
        user_adventure = UserAdventure.query.filter_by(user_id=current_user.id).first()
        stat = AttrInfo.query.filter_by(user_adventure_id=user_adventure.id, alias=alias).first()
        if stat.value > 0:
            stat.value -= 1
            db.session.commit()
    return jsonify({}), 200
