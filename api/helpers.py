from bottle import request

def get_session():
    return request.environ.get('beaker.session')

def user_id():
    session = get_session()
    return session['user_id']
