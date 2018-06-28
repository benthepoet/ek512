from bottle import get, HTTPError, request, response

from api.helpers import user_id
from api.middleware import authenticated
import lib.users as users

@get('/users/me')
@authenticated
def me():
    try:
        return users.get(user_id())
    except Exception:
        raise HTTPError(status=404)