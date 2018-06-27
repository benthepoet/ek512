import bcrypt
from bottle import HTTPError
from peewee import IntegrityError

from lib.models import User

def register(email, password):
    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    try:
        user = User.create(username=email, email=email, hash=hash)
        return user.id
    except IntegrityError:
        raise HTTPError(status=409)

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