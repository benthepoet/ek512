import falcon

import lib.helpers as helpers
import lib.security as security

class Confirm(object):
    def on_post(self, req, resp):
        data = req.media
        security.send_confirm_email(**data)
        resp.status = falcon.HTTP_204

class ConfirmToken(object):
    def on_post(self, req, resp, token):
        security.confirm_user(token)
        resp.status = falcon.HTTP_204

class Login(object):
    def on_post(self, req, resp):
        data = req.media
        user_id, token = security.authenticate(**data)
        user = security.get_user(user_id)
        resp.body = helpers.to_json(dict(user, token=token.decode()))
        
class Reset(object):
    def on_post(self, req, resp):
        data = req.media
        security.send_reset_email(**data)
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