import falcon

from playhouse.shortcuts import model_to_dict, update_model_from_dict

from lib.models import Document, Element

def create(user_id, data):
    document = Document.create(**dict(data, owner=user_id))
    return model_to_dict(document, recurse=False)

def create_element(user_id, document_id, data):
    document = select_document(user_id, document_id)
    element = Element.create(**dict(data, document_id=document.id))
    return model_to_dict(element, recurse=False)

def find(user_id, search=''):
    return list(
        select_documents(user_id)
        .where(Document.name.contains(search))
        .dicts()
    )
    
def find_elements(user_id, document_id):
    return list(
        select_document(user_id, document_id)
        .elements
        .dicts()
    )
    
def get(user_id, document_id):
    document = select_document(user_id, document_id)
    return model_to_dict(document, recurse=False)

def select_documents(user_id):
    return (
        Document
        .select()
        .where(Document.owner == user_id)
    )
    
def select_document(user_id, document_id):
    try:
        document = (
            select_documents(user_id)
            .where(Document.id == document_id)
            .get()
        )
    except Document.DoesNotExist:
        raise falcon.HTTPNotFound(description='The document does not exist.')
        
    return document
    
def select_element(user_id, document_id, element_id):
    document = select_document(user_id, document_id)
    
    try:
        element = (
            document
            .elements
            .where(Element.id == element_id)
            .get()
        )
    except Element.DoesNotExist:
        raise falcon.HTTPNotFound(description='The element does not exist.')
        
    return element

def update(user_id, document_id, data):
    document = select_document(user_id, document_id)
    update_model_from_dict(document, data)
    document.save()
    return model_to_dict(document, recurse=False)

def update_element(user_id, document_id, element_id, data):
    element = select_element(user_id, document_id, element_id)
    update_model_from_dict(element, data)
    element.save()
    return model_to_dict(element, recurse=False)