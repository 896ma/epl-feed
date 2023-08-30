import os
from dotenv import load_dotenv

load_dotenv()
from datetime import datetime

import peewee
import psycopg2


db = peewee.PostgresqlDatabase(os.environ.get('POSTGRES_URI', None))


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Post(BaseModel):
    uri = peewee.CharField(index=True)
    cid = peewee.CharField()
    reply_parent = peewee.CharField(null=True, default=None)
    reply_root = peewee.CharField(null=True, default=None)
    indexed_at = peewee.DateTimeField(default=datetime.now)


class SubscriptionState(BaseModel):
    service = peewee.CharField(unique=True)
    cursor = peewee.IntegerField()


if db.is_closed():
    db.connect()
    db.create_tables([Post, SubscriptionState])
