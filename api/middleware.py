from bottle import HTTPError, request

import lib.users as users

def authenticated(func):
    def func_wrapper():
        session = request.environ.get('beaker.session')
    
        if 'user_id' in session:    
            return func()
            
        raise HTTPError(status=401)
    return func_wrapper
    
def superuser(func):
    def func_wrapper():
        session = request.environ.get('beaker.session')
        user = users.get(session['user_id'])
        
        if user['is_superuser']:
            return func()
            
        raise HTTPError(status=403)
    return func_wrapper
            