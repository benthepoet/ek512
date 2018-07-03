import os
import time
import uuid
from peewee import *

database_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = database_proxy

class Role(BaseModel):
    name = CharField()

class User(BaseModel):
    email = CharField(unique=True)
    hash = BlobField()
    confirmed_at = TimestampField(null=True)
    created_at = TimestampField(default=time.time)
    reset_key = UUIDField(default=uuid.uuid4)

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
    document = ForeignKeyField(Document, backref='elements')
    element_type = ForeignKeyField(ElementType)
    x = IntegerField()
    y = IntegerField()
    width = IntegerField(default=0, constraints=[Check('width >= 0')])
    height = IntegerField(default=0, constraints=[Check('height >= 0')])
    radius = IntegerField(default=0, constraints=[Check('radius >= 0')])

build_env = os.environ.get('BUILD_ENV')
if build_env == 'test':
    database = SqliteDatabase(':memory:')
else:
    database = SqliteDatabase('db.sqlite')

database_proxy.initialize(database)
database.create_tables([
    Document,
    Element,
    ElementType,
    Role, 
    User,
    UserRole
])
