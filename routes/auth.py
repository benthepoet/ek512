from bottle import HTTPError, post, request, response

import lib.security as security

@post('/auth/signup')
def signup():
    data = request.json
    
    if data is None or not {'email', 'password'}.issubset(data):
        raise HTTPError(status=400)
        
    security.create_user(**data)
    response.status = 204

@post('/auth/login')
def login():
    data = request.json

    if data is None or not {'email', 'password'}.issubset(data):
        raise HTTPError(status=400)

    token = security.authenticate(**data)
    
    return {
        'token': token
    }
