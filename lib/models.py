import time
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
    hash = BlobField()
    is_superuser = BooleanField(default=False)
    confirmed_at = TimestampField(null=True)
    created_at = TimestampField(default=time.time)
    reset_at = TimestampField(null=True)

class UserRole(BaseModel):
    user = ForeignKeyField(User)
    role = ForeignKeyField(Role)

class Document(BaseModel):
    name = CharField()
    owner = ForeignKeyField(User)
    width = IntegerField(constraints=[Check('width > 0')])
    height = IntegerField(constraints=[Check('height > 0')])
    created_at = TimestampField(default=time.time)

class ElementType(BaseModel):
    name = CharField()

class Element(BaseModel):
    document = ForeignKeyField(Document)
    element_type = ForeignKeyField(ElementType)
    x = IntegerField()
    y = IntegerField()
    width = IntegerField(default=0, constraints=[Check('width > 0')])
    height = IntegerField(default=0, constraints=[Check('height > 0')])
    radius = IntegerField(default=0, constraints=[Check('radius > 0')])

database.create_tables([
    Document,
    Element,
    ElementType,
    Permission, 
    Role, 
    RolePermission, 
    User,
    UserRole
])
