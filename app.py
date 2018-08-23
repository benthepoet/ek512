import falcon
import falcon_cors
import os

from lib.models import *

import resources.auth as auth
import resources.documents as documents
import resources.users as users

import seeds.test as seed

db_filename = os.environ.get('DB_FILENAME') or ':memory:'

database.init(db_filename, pragmas={'journal_mode': 'wal'})
database.create_tables([Document, Element, ElementType, Role, User, UserRole])

if db_filename == ':memory:':
    seed.run()

cors = falcon_cors.CORS(allow_all_headers=True, allow_all_methods=True, allow_all_origins=True)
api = falcon.API(middleware=[cors.middleware])

api.add_route('/auth/confirm', auth.Confirm())
api.add_route('/auth/confirm/{token}', auth.ConfirmToken())
api.add_route('/auth/login', auth.Login())
api.add_route('/auth/reset', auth.Reset())
api.add_route('/auth/reset/{token}', auth.ResetToken())
api.add_route('/auth/signup', auth.SignUp())

api.add_route('/documents', documents.DocumentCollection())
api.add_route('/documents/{document_id}', documents.Document())
api.add_route('/documents/{document_id}/elements', documents.ElementCollection())
api.add_route('/documents/{document_id}/elements/{element_id}', documents.Element())

api.add_route('/users/me', users.Me())