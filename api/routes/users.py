from bottle import get, HTTPError, request, response

from api.middleware import authenticated
import lib.users as users

@get('/users/me')
@authenticated
def me():
    session = request.enivron.get('beaker.session')
    
    try:
        return users.get(session['user_id'])
    except Exception:
        raise HTTPError(status=404)