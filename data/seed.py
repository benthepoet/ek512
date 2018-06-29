from lib.models import *
import lib.security as security

def run():
    editor_role = Role.create(name='Editor')
    
    editor_id = security.create_user(email='editor@home.com', password='abc123')
    editor = User[editor_id]
    editor.save()
    
    UserRole.create(user=editor, role=editor_role)
    
    superuser_role = Role.create(name='Superuser')
    
    superuser_id = security.create_user(email='superuser@home.com', password='def456')
    superuser = User[superuser_id]
    superuser.save()
    
    UserRole.create(user=superuser, role=superuser_role)