import bcrypt
import falcon
import jwt
import time
import uuid
from itsdangerous import URLSafeTimedSerializer

from lib.models import User

TOKEN_MAX_AGE = 3600

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
        raise falcon.HTTPError(falcon.HTTP_401)

def confirm_user(token):
    try:
        user_id = confirm_serializer.loads(token, max_age=TOKEN_MAX_AGE)
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_400)
        
    user = get_user(user_id)
    
    if user.confirmed_at is not None:
        raise falcon.HTTPError(falcon.HTTP_409)
    
    user.confirmed_at = time.time()
    user.save()

def create_user(email, password):
    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        user = User.create(email=email, hash=hash)
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_409)
        
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
    try:
        user_id, reset_key = reset_serializer.loads(token, max_age=TOKEN_MAX_AGE)
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_400)
    
    user = get_user(user_id, False)
    
    if reset_key != user.reset_key:
        raise falcon.HTTPError(falcon.HTTP_409)
    
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