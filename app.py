import falcon

import resources.auth as auth

api = falcon.API()
api.add_route('/auth/login', auth.Login())
api.add_route('/auth/signup', auth.SignUp())