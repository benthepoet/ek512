import falcon

import resources.auth as auth
import resources.documents as documents
import resources.users as users

api = falcon.API()

api.add_route('/auth/confirm/{token}', auth.Confirm())
api.add_route('/auth/login', auth.Login())
api.add_route('/auth/reset/{token}', auth.Reset())
api.add_route('/auth/signup', auth.SignUp())

api.add_route('/documents', documents.DocumentCollection())
api.add_route('/documents/{document_id}', documents.Document())
api.add_route('/documents/{document_id}/elements', documents.ElementCollection())
api.add_route('/documents/{document_id}/elements/{element_id}', documents.Element())

api.add_route('/users/me', users.Me())