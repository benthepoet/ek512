import falcon

import lib.security as security

class Confirm(object):
    def on_post(self, req, resp):
        data = req.media
        security.send_confirm_email(data['email'])
        resp.status = falcon.HTTP_204

class ConfirmToken(object):
    def on_post(self, req, resp, token):
        security.confirm_user(token)
        resp.status = falcon.HTTP_204

class Login(object):
    def on_post(self, req, resp):
        data = req.media
        token = security.authenticate(**data)
        resp.media = dict(token=token.decode())
        
class Reset(object):
    def on_post(self, req, resp):
        data = req.media
        security.send_reset_email(data['email'])
        resp.status = falcon.HTTP_204
        
class ResetToken(object):
    def on_post(self, req, resp, token):
        security.reset_password(token)
        resp.status = falcon.HTTP_204
        
class SignUp(object):
    def on_post(self, req, resp):
        data = req.media
        security.create_user(**data)
        resp.status = falcon.HTTP_204