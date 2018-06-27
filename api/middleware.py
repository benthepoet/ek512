from bottle import HTTPError, request

from api.helpers import get_session, user_id
import lib.users as users

def authenticated(func):
    def func_wrapper(*args, **kwargs):
        session = get_session()

        if 'user_id' in session:    
            return func(*args, **kwargs)

        raise HTTPError(status=401)
    return func_wrapper

def superuser(func):
    def func_wrapper():
        user = users.get(user_id())

        if user['is_superuser']:
            return func()

        raise HTTPError(status=403)
    return func_wrapper
            