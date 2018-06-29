from bottle import get, HTTPError, post, request

from lib.helpers import authorize
import lib.documents as documents

@get('/documents')
@authorize
def find(user_id):
    return {
        'data': documents.find(user_id)
    }

@post('/documents')
@authorize
def create(user_id):
    data = request.json
    return documents.create(owner=user_id, **data)

@get('/documents/<document_id:int>')
@authorize
def document(user_id, document_id):
    try:
        return documents.get(user_id, document_id)
    except Exception:
        raise HTTPError(status=404)

@get('/documents/<document_id:int>/elements')
@authorize
def elements(user_id, document_id):
    return {
        'data': documents.get_elements(user_id, document_id)
    }

@post('/documents/<document_id:int>/elements')
@authorize
def create_element(user_id, document_id):
    data = request.json
    return documents.create_element(document=document_id, **data)
