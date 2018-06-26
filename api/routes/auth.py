from bottle import HTTPError, post, request, response

from lib.auth import authenticate

@post('/auth')
def auth():
    data = request.json
    
    if data is None or not {'email', 'password'}.issubset(data):
        raise HTTPError(status=400, body='The data is incomplete.')
    
    user_id = authenticate(data['email'], data['password'])
    
    if user_id is None:
        raise HTTPError(status=401, body='Authentication failed.')

    session = request.environ.get('beaker.session')
    session['user_id'] = user_id
    session.save()
    
    response.status = 204