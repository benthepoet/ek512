from peewee import *

database = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = database
        
class User(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    
database.create_tables([User])
