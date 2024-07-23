from flask import g, current_app
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy
from werkzeug.security import generate_password_hash


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


db = LocalProxy(get_db)


def count_sets():
    return db.get_collection('sets').estimated_document_count()


def get_set(set_id):
    try:
        pipeline = [{"$match": {"set_id": set_id}}]
        res = db.sets.aggregate(pipeline).next()
        res['words_count'] = count_words_in_set(res['set_id'])
        return res

    except StopIteration as _:
        return None

    except Exception as e:
        return {}


def get_all_sets():
    result = []

    cursor = db.sets.find({})
    for document in cursor:
        doc = document.copy()
        del doc['_id']
        doc['words_count'] = count_words_in_set(document['set_id'])
        del doc['words']

        result.append(doc)
    return result


def count_words_in_set(set_id):
    return len(db.sets.find({'set_id': set_id})[0]['words'])


def last_words_id(set_id):
    words = db.sets.find({'set_id': set_id})[0]['words']
    length = len(words)
    if length == 0:
        return 0
    return words[length - 1]['words_id']


def set_exists(set_id):
    if list(db.sets.find({'set_id': set_id})):
        return True
    return False


def create_set(set_id, name, lang_1, lang_2):
    set_doc = {'set_id': set_id, 'name': name, 'lang_1': lang_1, 'lang_2': lang_2, 'words': []}
    return db.sets.insert_one(set_doc)


def delete_set_by_id(set_id):
    return db.sets.delete_one({'set_id': set_id})


def update_set(set_id, name, lang_1, lang_2):
    return db.sets.update_one({'set_id': set_id}, {'$set': {'name': name, 'lang_1': lang_1, 'lang_2': lang_2}})


def add_words(set_id, new_words):
    return db.sets.update_one({'set_id': set_id}, {'$push': {'words': new_words}})


def delete_words_by_id(set_id, words_id):
    return db.sets.update_one({'set_id': set_id}, {'$pull': {'words': {'words_id': words_id}}})


def delete_all_words(set_id):
    return db.sets.update_one({'set_id': set_id}, {'$set': {'words': []}})


def update_words(set_id, new_words):
    return db.sets.update_one({'set_id': set_id},
                              {'$set': {'words.$[xxx]': new_words}},
                              array_filters=[{'xxx.words_id': new_words['words_id']}])


def count_users():
    return db.get_collection('users').estimated_document_count()


def create_user(username, email, password):
    users = db.users
    hashed_password = generate_password_hash(password)

    count = count_users()
    while list(users.find({'user_id': count})):
        count += 1

    users.insert_one({
        'user_id': count,
        'username': username,
        'email': email,
        'password': hashed_password
    })

    return count # user_id dodanego użytkownika


def get_user_by_email(email):
    return db.users.find_one({'email': email})
