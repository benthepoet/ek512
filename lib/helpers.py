import datetime
import decimal
import falcon
import json
import jwt
import uuid

def authorize(func):
    def func_wrapper(*args, **kwargs):
        req = args[1]
        header = req.env.get('HTTP_AUTHORIZATION')
        
        if not header:
            raise falcon.HTTPUnauthorized(description='No authorization header was found.')
            
        token = header.split(' ').pop()
        
        try:
            claims = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception:
            raise falcon.HTTPUnauthorized(description='The token is invalid or expired.')
        
        return func(*args, **dict(kwargs, user_id=claims['user_id']))
    return func_wrapper

def json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    elif isinstance(obj, uuid.UUID):
        return str(obj)

    raise TypeError('Cannot serialize {!r} (type {})'.format(obj, type(obj)))

def to_json(data):
    return json.dumps(data, default=json_serializer)