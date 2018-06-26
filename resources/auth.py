import bottle

@bottle.post('/auth')
def auth():
    return dict()