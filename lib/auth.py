from passlib.hash import pbkdf2_sha256

from lib.models import Login, User

def authenticate(email, password):
    login = (Login
            .select()
            .join(User)
            .where(User.email == email)
            .get())
            
    hash = pbkdf2_sha256.hash(password)
    
    login.user_id if pbkdf2_sha256.verify(hash, login.hash) else None