from bottle import get, HTTPError, post, request

from lib.helpers import authorize
import lib.documents as documents

@get('/documents')
@authorize
def find(user_id):
    return documents.find(user_id)

@post('/documents')
@authorize
def create():
    data = request.json
    return documents.create(**data)

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
    return documents.get_elements(user_id, document_id)
