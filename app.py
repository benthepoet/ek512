import falcon

import resources.auth as auth

api = falcon.API()
api.add_route('/auth/login', auth.Login())