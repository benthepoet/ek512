import bottle
from passlib.hash import pbkdf2_sha256

from lib.models import Login, User

@bottle.get('/auth')
def auth():
    data = bottle.request.json
    
    try:
        login = (Login
                .select()
                .join(User)
                .where(User.email == data['email'])
                .dicts()
                .get())
                
        hash = pbkdf2_sha256.hash(data['password'])
        if not pbkdf2_sha256.verify(hash, login['hash']):
            raise Exception('The user could not be authenticated.')
            
        return {
            'data': 'Authenticated'
        }
    except Exception as e:
        return {
            'error': str(e)
        }