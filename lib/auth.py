import bcrypt
from bottle import HTTPError
from itsdangerous import URLSafeTimedSerializer
from peewee import IntegrityError

from lib.models import User

confirm_serializer = URLSafeTimedSerializer()
reset_serializer = URLSafeTimedSerializer()

def confirm(token):
    user_id = confirm_serializer.loads(token, max_age=3600)
    return

def generate_confirm(user_id):
    return confirm_serializer.dumps(user_id)

def generate_reset(user_id):
    return reset_serializer.dumps(user_id)

def register(email, password):
    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        user = User.create(username=email, email=email, hash=hash)
        return user.id
    except IntegrityError:
        raise HTTPError(status=409)

def reset(token):
    user_id = reset_serializer.loads(token, max_age=3600)
    pass

def sign_in(email, password):
    try:
        user = (
            User
            .select()
            .where(User.username == email)
            .get()
        )

        if bcrypt.checkpw(password.encode(), user.hash):
            return user.id

        raise Exception()
    except Exception:
        raise HTTPError(status=401)