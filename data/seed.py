from lib.models import *
import lib.auth as auth

def run():
    editor_role = Role.create(name='Editor')
    
    permissions = [
        { 'name': 'document.read' },
        { 'name': 'document.write' },
        { 'name': 'document.element.read' },
        { 'name': 'document.element.write' }
    ]
    
    for data in permissions:
        permission = Permission.create(**data)
        RolePermission.create(role=editor_role.id, permission=permission.id)
    
    editor_id = auth.register(email='editor@home.com', password='abc123')
    editor = User[editor_id]
    editor.save()
    
    UserRole.create(user=editor, role=editor_role)
    
    superuser_id = auth.register(email='superuser@home.com', password='def456')
    superuser = User[superuser_id]
    superuser.is_superuser = True
    superuser.save()