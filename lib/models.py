from peewee import *

database = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = database
        
class Permission(BaseModel):
    name = CharField()

class Role(BaseModel):
    name = CharField()
        
class RolePermission(BaseModel):
    permission = ForeignKeyField(Permission)
    role = ForeignKeyField(Role)
        
class User(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    username = CharField()
    password = CharField()
    
class UserRole(BaseModel):
    user = ForeignKeyField(User)
    role = ForeignKeyField(Role)
    
database.create_tables([
    Permission, 
    Role, 
    RolePermission, 
    User,
    UserRole
])
