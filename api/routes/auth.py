from bottle import HTTPError, post, request, response

import lib.auth as auth

@post('/auth/register')
def register():
    data = request.json
    
    if data is None or not {'email', 'password'}.issubset(data):
        raise HTTPError(status=400)
        
    user_id = auth.register(data['email'], data['password'])

    if user_id is None:
        raise HTTPError(status=401)
        
    init_session(user_id)
    
    response.status = 204

@post('/auth/sign-in')
def sign_in():
    data = request.json

    if data is None or not {'email', 'password'}.issubset(data):
        raise HTTPError(status=400)

    user_id = auth.sign_in(data['email'], data['password'])

    if user_id is None:
        raise HTTPError(status=401)

    init_session(user_id)    

    response.status = 204
    
def init_session(user_id):
    session = request.environ.get('beaker.session')
    session['user_id'] = user_id
    session.save()