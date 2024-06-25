import requests

BASE = 'http://127.0.0.1:5000/api/v1/fishki'

response = requests.post(BASE + '/create_set', json={'name': 'First set', 'lang_1': 'pl', 'lang_2': 'it'})


# words = [('kot', 'un gatto'), ('plecak', 'uno zaino'), ('pies', 'un cane'), ('pokój', 'una stanza')]
# for i in range(len(words)):
#     response = requests.post(BASE + '/add_words', json={'set_id': 1, 'word_1': words[i][0], 'word_2': words[i][1]})

print(response.json())
