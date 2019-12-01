"""Contains application views"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_user, login_required

from livebook.extensions import bcrypt
from livebook.models import User, db, UserAdventure, AttrInfo
from livebook.parsers.google_sheets.parser import read_stats, read_initial_scenes, get_scene_names, read_scene, \
    spreadsheet_id

views = Blueprint('views', __name__)  # pylint: disable=invalid-name

# Variables used for caching information about the presented adventure
stats = None
start_scene = None
end_scenes = None
scene_names = None
scenes = None


@views.before_app_first_request
def prepare_cache():
    """
    Function that runs on the first request and caches information on the adventure
    """
    # We only have a single adventure planned, so this should do decently enough
    # Also, slows down the first access to the page
    global stats
    global start_scene
    global end_scenes
    global scene_names
    global scenes

    stats = read_stats()
    start_scene, end_scenes = read_initial_scenes()
    scene_names = get_scene_names()
    scenes = {scene: get_scene(scene) for scene in scene_names}


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
        new_user = User(
            email=data['email'],
            password=bcrypt.generate_password_hash(
                data['password']).decode(),
            admin=False)
        db.session.add(new_user)

        # TODO: currently we only support one adventure and create the base at registration.
        #  Probably better redo this part
        new_adventure = UserAdventure(
            user=new_user,
            adventure=spreadsheet_id,
            scene=start_scene)
        db.session.add(new_adventure)
        db.session.commit()

        for stat in stats:
            new_stat = AttrInfo(
                user_adventure_id=new_adventure.id,
                alias=stat.alias,
                value=stat.default_value)
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
    if user is not None and bcrypt.check_password_hash(
            user.password, data['password']):
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


@views.route('/player', methods=['GET'])
def get_player():
    """
    Returns information about the currently authorized player
    :return: player id, current player scene and player current stats
        with values with HTTP code 200 on success
        HTTP code 401 if no user is authorized at the current session
    """
    out = {}
    return_code = 401

    if current_user is not None and current_user.is_authenticated:
        user_adventure = UserAdventure.query.filter_by(
            user_id=current_user.id).first()
        user_stats = AttrInfo.query.filter_by(
            user_adventure_id=user_adventure.id).all()

        out['id'] = current_user.id
        out['current_scene'] = user_adventure.scene
        out['current_stats'] = dict()
        for stat in user_stats:
            out['current_stats'][stat.alias] = stat.value
        return_code = 200

    return jsonify(out), return_code


@views.route('/adventure', methods=['GET'])
def get_adventure():
    """
    Returns the information about the adventure
    :return: stat information, names of all the scenes, starting and ending scenes
    """
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
    """
    Returns the next scene for the user based on the picked option
    :param index: Index of the option in the current scene
    :return: information on the next scene after the option, with the prompt text, HTTP code 200
        HTTP code 401 if no user is authorized at the current session
        HTTP code 400 if the user is in incorrect scene or the index is incorrect
    """
    out = {}
    return_code = 401

    if current_user is not None and current_user.is_authenticated:
        return_code = 400
        user_adventure = UserAdventure.query.filter_by(
            user_id=current_user.id).first()
        scene = scenes.get(user_adventure.scene, None)
        if scene is not None:
            if scene['options'].get(index, None) is not None:
                out = scenes[scene['options'][index]['next']]
                out['description'] = scene['options'][index]['prompt'] + \
                    '\n' + out['description']

                user_adventure.scene = scene['options'][index]['next']
                db.session.commit()
                return_code = 200

    return jsonify(out), return_code


@views.route('/adventure/scene/<string:scene>', methods=['GET'])
def return_scene(scene):
    """
    Returns information on the scene
    :param scene: scene name
    :return: scene text, option information, HTTP code 200
        HTTP code 400 if the scene name is incorrect
    """
    scene_data = scenes.get(scene, {})
    return_code = 400
    if scene_data != {}:
        return_code = 200
    return jsonify(scene_data), return_code


@views.route('/increase/<string:alias>', methods=['POST'])
def increase_stat(alias):
    """
    Raises the current player's stat by 1
    :param alias: alias of the stat
    :return: HTPP code 200 on success
        HTTP code 401 if no user is authorized at the current session
    """
    return_code = 401
    if current_user is not None and current_user.is_authenticated:
        user_adventure = UserAdventure.query.filter_by(
            user_id=current_user.id).first()
        stat = AttrInfo.query.filter_by(
            user_adventure_id=user_adventure.id,
            alias=alias).first()
        stat.value += 1
        db.session.commit()
        return_code = 200
    return jsonify({}), return_code


@views.route('/decrease/<string:alias>', methods=['POST'])
def decrease_stat(alias):
    """
    Lowers the current player's stat by 1 if it's greater than 0
    :param alias: alias of the stat
    :return: HTPP code 200 on success
        HTTP code 401 if no user is authorized at the current session
    """
    return_code = 401
    if current_user is not None and current_user.is_authenticated:
        user_adventure = UserAdventure.query.filter_by(
            user_id=current_user.id).first()
        stat = AttrInfo.query.filter_by(
            user_adventure_id=user_adventure.id,
            alias=alias).first()
        return_code = 200
        if stat.value > 0:
            stat.value -= 1
            db.session.commit()
    return jsonify({}), return_code
