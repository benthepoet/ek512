from bottle import HTTPError, post, request, response

import lib.security as security

@post('/auth/confirm/<token>')
def confirm(token):
    security.confirm_user(token)
    response.status = 204

@post('/auth/login')
def login():
    data = request.json

    if data is None or not {'email', 'password'}.issubset(data):
        raise HTTPError(status=400)

    token = security.authenticate(**data)
    
    return dict(token=token.decode())
    
@post('/auth/reset/<token>')
def reset(token):
    security.reset_password(token)
    response.status = 204
    
@post('/auth/signup')
def signup():
    data = request.json
    
    if data is None or not {'email', 'password'}.issubset(data):
        raise HTTPError(status=400)
        
    security.create_user(**data)
    response.status = 204
