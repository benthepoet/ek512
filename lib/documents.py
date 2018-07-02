from playhouse.shortcuts import model_to_dict

from lib.models import Document, Element

def create(**data):
    document = Document.create(**data)
    return model_to_dict(document, recurse=False)

def create_element(data):
    return Element.create(**data)

def find(user_id):
    return (
        Document
        .select()
        .where(Document.owner == user_id)
        .dicts()
    )
    
def get(user_id, document_id):
    return (
        Document
        .select()
        .where(Document.id == document_id & Document.owner == user_id)
        .dicts()
        .get()
    )
    
def get_elements(user_id, document_id):
    return (
        Element
        .select()
        .join(Document)
        .where(Document.id == document_id & Document.owner == user_id)
    )
    
def update(user_id, document_id, document):
    return (
        Document
        .update(**document)
        .where(Document.id == document_id & Document.owner == user_id)
    )
    
def update_element(user_id, document_id, element):
    return (
        Element
        .update(**element)
        .join(Document)
        .where(Document.id == document_id & Document.owner == user_id)
        .execute()
    )