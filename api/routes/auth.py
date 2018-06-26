import bottle

from lib.models import User

@bottle.get('/auth')
def auth():
    users = (User
        .select()
        .where(User.id == 1)
        .dicts())
    
    return { 'data': list(users) }