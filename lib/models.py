import datetime
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
    hash = BlobField()
    is_active = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

class UserRole(BaseModel):
    user = ForeignKeyField(User)
    role = ForeignKeyField(Role)

class Document(BaseModel):
    name = CharField()
    width = IntegerField(constraints=[Check('width > 0')])
    height = IntegerField(constraints=[Check('height > 0')])
    owner = ForeignKeyField(User)
    created_at = TimestampField(default=datetime.datetime.now)

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
