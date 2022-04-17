from peewee import SqliteDatabase, Model

from config import dbfile

db = SqliteDatabase(None)
db.init(dbfile)

class BaseModel(Model):
    class Meta:
        database = db

