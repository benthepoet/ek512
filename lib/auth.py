import bcrypt

from lib.models import User

def register(email, password):
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
    user = User.create(username=email, email=email, password_hash=password_hash)
    return user.id

def sign_in(email, password):
    user = (
        User
        .select()
        .where(User.username == email)
        .get()
    )

    user.id if bcrypt.checkpw(password, user.password_hash) else None
