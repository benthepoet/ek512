from playhouse.shortcuts import model_to_dict

from lib.models import Document, Element

def user_document(func):
    def wrapper(*args, **kwargs):
        user_id, document_id = args

        if user_id and document_id:
            doc = get(user_id, document_id)
        
        return func(*args, **kwargs)
            
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

@user_document
def get_elements(user_id, document_id):
    return (
        Element
        .select()
        .where(Element.document == document_id)
        .dicts()
    )
    
def update(user_id, document_id, document):
    return (
        Document
        .update(**document)
        .where((Document.id == document_id) & (Document.owner == user_id))
    )
    
def update_element(user_id, document_id, element):
    return (
        Element
        .update(**element)
        .join(Document)
        .where((Document.id == document_id) & (Document.owner == user_id))
        .execute()
    )