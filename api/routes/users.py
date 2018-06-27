from bottle import get, HTTPError, request, response

from api.helpers import get_user_id
from api.middleware import authenticated
import lib.users as users

@get('/users/me')
@authenticated
def me():
    user_id = get_user_id()
    
    try:
        return users.get(user_id)
    except Exception:
        raise HTTPError(status=404)