from flask import g, current_app
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


db = LocalProxy(get_db)
