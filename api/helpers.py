from bottle import request

def get_user_id():
    session = request.environ.get('beaker.session')
    return session['user_id']