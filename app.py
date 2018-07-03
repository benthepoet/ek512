import falcon

import resources.auth as auth
import resources.documents as documents

api = falcon.API()
api.add_route('/auth/confirm/{token}', auth.Confirm())
api.add_route('/auth/login', auth.Login())
api.add_route('/auth/reset/{token}', auth.Reset())
api.add_route('/auth/signup', auth.SignUp())

api.add_route('/documents', documents.DocumentCollection())