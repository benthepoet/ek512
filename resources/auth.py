import datetime
import decimal
import falcon
import json

import lib.security as security

class Confirm(object):
    def on_post(self, req, resp, token):
        security.confirm_user(token)
        resp.status = falcon.HTTP_204

class Login(object):
    def on_post(self, req, resp):
        data = req.media

        if data is None or not {'email', 'password'}.issubset(data):
            raise falcon.HTTPError(falcon.HTTP_400)
    
        token = security.authenticate(**data)
        
        resp.media = dict(token=token.decode())
        
class Reset(object):
    def on_post(self, req, resp, token):
        security.reset_password(token)
        resp.status = falcon.HTTP_204
        
class SignUp(object):
    def on_post(self, req, resp):
        data = req.media
    
        if data is None or not {'email', 'password'}.issubset(data):
            raise falcon.HTTPError(falcon.HTTP_400)
            
        security.create_user(**data)
        resp.status = falcon.HTTP_204