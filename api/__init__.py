import bottle
import uuid
from beaker.middleware import SessionMiddleware

from api.routes import auth, documents, users

session_opts = {
    'session.type': 'cookie',
    'session.same_site': True,
    'session.validate_key': uuid.uuid4()
}

app = SessionMiddleware(bottle.app(), session_opts)