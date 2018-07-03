import time
import uuid
from peewee import *

database = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = database

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