from passlib.hash import pbkdf2_sha256

from lib.models import User

def authenticate(email, password):
    user = (
        User
        .select()
        .where(User.email == email)
        .get()
    )
            
    hash = pbkdf2_sha256.hash(password)
    
    user.id if pbkdf2_sha256.verify(hash, user.password) else None