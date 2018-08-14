import json
import time
import uuid
from peewee import *

database = SqliteDatabase(None)

class JSONField(TextField):

    def db_value(self, value):
        return json.dumps(value)
        
    def python_value(self, value):
        return json.loads(value)

class BaseModel(Model):
    class Meta:
        database = database

class Role(BaseModel):
    name = CharField()

class User(BaseModel):
    email = CharField(unique=True)
    hash = BlobField()
    confirmed_at = TimestampField(default=None, null=True)
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
    attributes = JSONField()