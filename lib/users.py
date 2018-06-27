from lib.models import Permission, Role, RolePermission, User, UserRole

def get(user_id):
    user = (
        User
        .dicts()
        .get(User.id == user_id)
    )
    
    user.pop('hash', None)
    return user
    
def has_permission(user_id, name):
    try:
        permission = (
            Permission
            .select()
            .join(RolePermission)
            .join(Role)
            .join(UserRole)
            .where(UserRole.user_id == user_id)
            .get()
        )
        
        return True
    except Exception:
        return False
    
    