import datetime
import decimal
import falcon
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
        
class Document(object):
    @helpers.authorize
    def on_get(self, req, resp, user_id, document_id):
        try:
            resp.body = helpers.to_json(documents.get(user_id, document_id))
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_404)
            
    @helpers.authorize
    def on_put(self, req, resp, user_id, document_id):
            data = req.media
    
            try:
                resp.body = helpers.to_json(dict(data=documents.update(user_id, document_id, data)))
            except Exception:
                raise falcon.HTTPError(falcon.HTTP_404)
                
class ElementCollection(object):
    @helpers.authorize
    def on_get(self, req, resp, user_id, document_id):
        try:
            resp.body = helpers.to_json(dict(data=documents.find_elements(user_id, document_id)))
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_404)
            
    @helpers.authorize
    def on_post(self, req, resp, user_id, document_id):
        data = req.media
        return documents.create_element(**data)
        
class Element(object):
    @helpers.authorize
    def on_put(self, req, resp, user_id, document_id, element_id):
        data = req.media
    
        try:
            resp.body = helpers.to_json(dict(data=documents.update_element(user_id, document_id, element_id, data)))
        except Exception:
            raise falcon.HTTPError(falcon.HTTP_404)