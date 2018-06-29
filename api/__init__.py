import bottle
import uuid
from beaker.middleware import SessionMiddleware

from routes import auth, documents, users

session_opts = {
    'session.type': 'cookie',
    'session.same_site': 'Lax',
    'session.validate_key': uuid.uuid4()
}

app = SessionMiddleware(bottle.app(), session_opts)