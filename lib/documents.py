from playhouse.shortcuts import model_to_dict, update_model_from_dict

from lib.models import Document, Element

def select_all(user_id):
    return (
        Document
        .select()
        .where(Document.owner == user_id)
    )
    
def select_one(user_id, document_id):
    return (
        select_all(user_id)
        .where(Document.id == document_id)
        .get()
    )

def create(**data):
    document = Document.create(**data)
    return model_to_dict(document, recurse=False)

def create_element(data):
    element = Element.create(**data)
    return model_to_dict(element, recurse=False)

def find(user_id):
    return list(select_all(user_id).dicts())
    
def find_elements(user_id, document_id):
    return list(
        select_one(user_id, document_id)
        .elements
        .dicts()
    )
    
def get(user_id, document_id):
    return model_to_dict(select_one(user_id, document_id), recurse=False)

def update(user_id, document_id, data):
    document = select_one(user_id, document_id)
    update_model_from_dict(document, data)
    document.save()
    return model_to_dict(document, recurse=False)

def update_element(user_id, document_id, element_id, data):
    element = (
        select_one(user_id, document_id)
        .elements
        .where(Element.id == element_id)
        .get()
    )
    update_model_from_dict(element, data)
    element.save()
    return model_to_dict(element, recurse=False)