import bcrypt
import jwt
import time
import uuid
from bottle import HTTPError
from itsdangerous import URLSafeTimedSerializer

from lib.models import User

confirm_serializer = URLSafeTimedSerializer(uuid.uuid4())
reset_serializer = URLSafeTimedSerializer(uuid.uuid4())

def authenticate(email, password):
    try:
        user = User.get(User.email == email)

        if not bcrypt.checkpw(password.encode(), user.hash):
            raise Exception()
            
        claims = {
            'user_id': user.id,
            'iss': time.time()
        }
    
        return jwt.encode(claims, 'secret', algorithm='HS256')
    except Exception:
        raise HTTPError(status=401)

def confirm_user(token):
    user_id = confirm_serializer.loads(token, max_age=3600)
    user = get_user(user_id)
    
    if user.confirmed_at is not None:
        raise HTTPError(status=409)
    
    user.confirmed_at = time.time()
    user.save()
    
    return True

def create_user(email, password):
    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        user = User.create(email=email, hash=hash)
    except Exception:
        raise HTTPError(status=409)
        
    return user

def get_confirm_token(email):
    user = User.get(User.email == email)
    return confirm_serializer.dumps(user.id)

def get_reset_token(email):
    user = User.get(User.email == email)
    return reset_serializer.dumps((user.id, user.reset_key))

def get_user(user_id, safe=True):
    user = User.get(User.id == user_id)
    
    if safe:
        user.pop('hash', None)
    
    return user

def reset_password(token, password):
    user_id, reset_key = reset_serializer.loads(token, max_age=3600)
    user = get_user(user_id, False)
    
    if reset_key != user.reset_key:
        raise HTTPError(status=409)
    
    user.hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user.reset_key = uuid.uuid4()
    user.save()

def update_password(user_id, password, new_password):
    user = get_user(user_id, False)
    
    if not bcrypt.checkpw(password.encode(), user.hash):
        raise Exception()
        
    user.hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    user.reset_key = uuid.uuid4()
    user.save()