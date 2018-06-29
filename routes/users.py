from bottle import get, HTTPError

from api.helpers import authorize
import lib.security as security

@get('/users/me')
@authorize
def me(user_id):
    try:
        return security.get_user(user_id)
    except Exception:
        raise HTTPError(status=404)