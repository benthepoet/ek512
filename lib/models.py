from peewee import *

database = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = database
        
class User(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    
class Login(BaseModel):
    hash = CharField()
    user = ForeignKeyField(User, unique=False, primary_key=True)
    
database.create_tables([Login, User])
