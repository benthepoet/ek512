from lib.models import Document, Element

def create(document):
    return Document.create(**document)

def create_element(user_id, element):
    document = get(user_id, element.document_id)
    return Element.create(**element)

def find(user_id):
    return (
        Document
        .select()
        .where(Document.owner == user_id)
    )
    
def get(user_id, document_id):
    return (
        Document
        .select()
        .where(Document.id == document_id & Document.owner == user_id)
        .get()
    )
    
def get_elements(user_id, document_id):
    return (
        Element
        .select()
        .join(Document)
        .where(Document.id == document_id & Document.owner == user_id)
    )
    
def update_document(user_id, document_id, document):
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