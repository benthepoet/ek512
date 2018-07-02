from playhouse.shortcuts import model_to_dict

from lib.models import Document, Element

def require_document(func):
    def wrapper(user_id, document_id, data):
        if user_id and document_id:
            get(user_id, document_id)
        
        return func(user_id, document_id, data)
            
    return wrapper

def create(**data):
    document = Document.create(**data)
    return model_to_dict(document, recurse=False)

def create_element(data):
    element = Element.create(**data)
    return model_to_dict(element, recurse=False)

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
        .where((Document.id == document_id) & (Document.owner == user_id))
        .dicts()
        .get()
    )

@require_document
def get_elements(user_id, document_id):
    return (
        Element
        .select()
        .where(Element.document == document_id)
        .dicts()
    )
 
@require_document
def update(user_id, document_id, data):
    return (
        Document
        .update(**data)
        .where(Document.id == document_id)
        .execute()
    )
    
@require_document
def update_element(user_id, document_id, data):
    return (
        Element
        .update(**data)
        .join(Document)
        .where(Document.id == document_id)
        .execute()
    )