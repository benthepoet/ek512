import falcon

import lib.security as security

class Login(object):
    def on_post(self, req, resp):
        data = req.media

        if data is None or not {'email', 'password'}.issubset(data):
            raise falcon.HTTPError(400)
    
        token = security.authenticate(**data)
        
        resp.media = dict(token=token.decode())