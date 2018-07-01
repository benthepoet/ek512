from lib.models import *
import lib.security as security

def run():
    editor_role = Role.create(name='Editor')
    
    editor_id = security.create_user(email='editor@home.com', password='abc123')
    editor = User[editor_id]
    editor.save()
    
    UserRole.create(user=editor, role=editor_role)
    
    editor_document = Document.create(name='My Document', owner=editor, width=512, height=512)
    circle_type = ElementType.create(name='Circle')
    circle_element = Element.create(document=editor_document, element_type=circle_type, x=0, y=0)
    
    superuser_role = Role.create(name='Superuser')
    
    superuser_id = security.create_user(email='superuser@home.com', password='def456')
    superuser = User[superuser_id]
    superuser.save()
    
    UserRole.create(user=superuser, role=superuser_role)
    
if __name__ == '__main__':
    run()