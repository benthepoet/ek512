import falcon
import os

from lib.models import *

import resources.auth as auth
import resources.documents as documents
import resources.users as users

import seeds.test as seed

db_filename = os.environ.get('DB_FILENAME') or ':memory:'

database.init(db_filename)
database.create_tables([Document, Element, ElementType, Role, User, UserRole])

if db_filename == ':memory:':
    seed.run()

api = falcon.API()

api.add_route('/auth/confirm', auth.Confirm())
api.add_route('/auth/confirm/{token}', auth.ConfirmToken())
api.add_route('/auth/login', auth.Login())
api.add_route('/auth/reset/{token}', auth.ResetToken())
api.add_route('/auth/signup', auth.SignUp())

api.add_route('/documents', documents.DocumentCollection())
api.add_route('/documents/{document_id}', documents.Document())
api.add_route('/documents/{document_id}/elements', documents.ElementCollection())
api.add_route('/documents/{document_id}/elements/{element_id}', documents.Element())

api.add_route('/users/me', users.Me())