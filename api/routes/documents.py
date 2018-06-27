from bottle import get, HTTPError

from api.helpers import get_user_id
import lib.documents as documents

@get('/documents')
def find():
    user_id = get_user_id()
    return documents.find(user_id)

@get('/documents/<document_id:int>')
def document(document_id):
    user_id = get_user_id()

    try:
        return documents.get(user_id, document_id)
    except Exception:
        raise HTTPError(status=404)

@get('/documents/<document_id:int>/elements')
def elements(document_id):
    user_id = get_user_id()
    return documents.get_elements(user_id, document_id)
