import bcrypt
import time
from bottle import HTTPError
from itsdangerous import URLSafeTimedSerializer
from peewee import IntegrityError

from lib.models import User

confirm_serializer = URLSafeTimedSerializer()
reset_serializer = URLSafeTimedSerializer()

def confirm(token):
    user_id = confirm_serializer.loads(token, max_age=3600)
    user = User.get(User.id == user_id)
    
    if user.confirmed_at is not None:
        raise HTTPError(status=409)
    
    user.confirmed_at = time.time()
    user.save()
    
    return True

def get_confirm_token(email):
    user = User.get(User.email == email)
    return confirm_serializer.dumps(user.id)

def get_reset_token(email):
    user = User.get(User.email == email)
    user.reset_at = time.time()
    user.save()
    
    return reset_serializer.dumps((user.id, user.reset_at))

def register(email, password):
    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        user = User.create(email=email, hash=hash)
        return user.id
    except IntegrityError:
        raise HTTPError(status=409)

def reset(token, password):
    user_id, reset_at = reset_serializer.loads(token, max_age=3600)
    user = User.get(User.id == user_id)
    
    if reset != user.reset_at:
        raise HTTPError(status=409)
    
    user.hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user.save()

def sign_in(email, password):
    try:
        user = User.get(User.email == email)

        if bcrypt.checkpw(password.encode(), user.hash):
            return user.id

        raise Exception()
    except Exception:
        raise HTTPError(status=401)