from flask import g, current_app
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


db = LocalProxy(get_db)


def count_sets():
    # print(db.get_collection('sets').estimated_document_count())
    return db.get_collection('sets').estimated_document_count()


def set_exists(set_id):
    if list(db.sets.find({'set_id': set_id})):
        return True
    return False


def create_set(set_id, name, lang_1, lang_2):
    set_doc = {'set_id': set_id, 'name': name, 'lang_1': lang_1, 'lang_2': lang_2, 'words': []}
    return db.sets.insert_one(set_doc)


def add_words(set_id, new_words):
    return db.sets.update_one({'set_id': set_id}, {'$push': {'words': new_words}})
