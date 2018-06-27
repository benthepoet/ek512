from lib.models import Document, Element

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
        .get()
    )
    
def get_elements(user_id, document_id):
    return (
        Element
        .select()
        .join(Document)
        .where(Document.id == document_id & Document.owner == user_id)
    )