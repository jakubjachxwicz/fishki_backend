import requests

BASE = 'http://127.0.0.1:5000/api/v1/fishki'

# response = requests.post(BASE + '/create_set', json={'name': 'First set', 'lang_1': 'pl', 'lang_2': 'it'})


# words = [('kot', 'un gatto'), ('plecak', 'uno zaino'), ('pies', 'un cane'), ('pokój', 'una stanza')]
# for i in range(len(words)):
#     response = requests.post(BASE + '/add_words', json={'set_id': 6, 'word_1': words[i][0], 'word_2': words[i][1]})

# response = requests.patch(BASE + '/update_set', json={'set_id': 2, 'name': 'Siała baba maKanapkak', 'lang_2': 'en'})

# response = requests.patch(BASE + '/update_words', json={'set_id': 3, 'words_id': 1, 'word_1': 'śpiewać', 'word_2': 'cantare'})

# response = requests.delete(BASE + '/delete_set', json={'set_id': 0})

# response = requests.delete(BASE + '/delete_words', json={'set_id': 3, 'words_id': 3})

# response = requests.delete(BASE + '/delete_all_words', json={'set_id': 1})

response = requests.get(BASE + '/get_set', json={'set_id': 2})

print(response.json())
