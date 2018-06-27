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
    email = CharField(unique=True)
    username = CharField(unique=True)
    password_hash = CharField()
    is_active = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

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
