import datetime
import decimal
import json

import lib.helpers as helpers
import lib.documents as documents

class DocumentCollection(object):
    @helpers.authorize
    def on_get(self, req, resp, user_id):
        resp.body = helpers.to_json(dict(data=documents.find(user_id)))
        
    @helpers.authorize
    def on_post(self, req, resp, user_id):
        data = req.media
        resp.body = helpers.to_json(documents.create(owner=user_id, **data))