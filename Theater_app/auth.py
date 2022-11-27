from itsdangerous import URLSafeTimedSerializer
from flask_login import login_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .settings import SECRET_KEY
serial = URLSafeTimedSerializer(SECRET_KEY)

class User(UserMixin):

    def __init__(self, member_data):
        self.member_data = member_data

    def get_id(self):
        return self.member_data['session_token']


def serial_dump(username, password):
    return serial.dumps([username, password])


def serial_load(session_token):
    return serial.loads(session_token, max_age=10000)


def create_user(db, username, password):
    user = db.find_one({'username': username})
    if not user:
        session_token = serial_dump(username, password)
        db.insert_one({'username': username, 'password': generate_password_hash(password),
                       'session_token': session_token})
        return True
    return False


def user_login(db, username, password):

    user = db.find_one({'username': username})
    if user:
        if check_password_hash(user['password'], password):
            s = serial_dump(username, password)
            edit_items = {'session_token': s}
            ud = db.update_one({'username': username}, {"$set": edit_items}, upsert=False)
            user = db.find_one({'username': username})
            userl = User(user)
            login_user(userl, remember=True)
            return True
    return False


def change_password(db, password, username):
    session_token = serial_dump(username, password)
    edit_items = ({'password': generate_password_hash(password), 'session_token': session_token})
    ud = db.update_one({'username': username}, {"$set": edit_items}, upsert=False)
    if ud:
        return True
    return False

