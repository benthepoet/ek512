import jwt
from bottle import HTTPError, request

def authorize(func):
    def func_wrapper(*args, **kwargs):
        header = request.environ.get('HTTP_AUTHORIZATION')
        
        if not header:
            raise HTTPError(status=401)
            
        token = header.split(' ').pop()
        
        try:
            claims = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception:
            raise HTTPError(status=401)
        
        return func(*args, **dict(kwargs, user_id=claims['user_id']))
    return func_wrapper