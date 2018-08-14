import time

from lib.models import *
import lib.security as security

def run():
    circle_type = ElementType.create(name='Circle')
    rect_type = ElementType.create(name='Rectangle')
    
    editor_role = Role.create(name='Editor')
    
    editor_id = security.create_user(email='editor@home.com', password='abc123')
    editor = User[editor_id]
    editor.confirmed_at = time.time()
    editor.save()
    
    UserRole.create(user=editor, role=editor_role)
    
    document = Document.create(name='First Document', owner=editor, width=512, height=512)
    Element.create(document=document, element_type=circle_type, attributes=dict(x=0, y=0, radius=50))
    
    document = Document.create(name='Second Document', owner=editor, width=640, height=480)
    Element.create(document=document, element_type=rect_type, attributes=dict(x=0, y=0, width=200, height=100))
    
    superuser_role = Role.create(name='Superuser')
    
    superuser_id = security.create_user(email='superuser@home.com', password='def456')
    superuser = User[superuser_id]
    superuser.confirmed_at = time.time()
    superuser.save()
    
    UserRole.create(user=superuser, role=superuser_role)
    
    document = Document.create(name='First Document', owner=superuser, width=256, height=256)
    Element.create(document=document, element_type=rect_type, attributes=dict(x=0, y=0, width=48, height=48))
    
if __name__ == '__main__':
    run()