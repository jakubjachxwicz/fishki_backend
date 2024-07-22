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

# response = requests.get(BASE + '/get_set', json={'set_id': 2})

# response = requests.get(BASE + '/get_all_sets')

# response = requests.get(BASE + '/get_words?set_id=2')

# response = requests.get(BASE + '/get_set?set_id=2')

# response = requests.delete(BASE + '/delete_set?set_id=5')

# response = requests.patch(BASE + '/update_set?set_id=4', json={'name': 'AAA', 'lang_1': 'bg', 'lang_2': 'pl'})

# words = [('kot', 'cat'), ('dough', 'ciasto'), ('cookie', 'ciastko'), ('swamp', 'bangno')]
for i in range(200):
    requests.post(BASE + '/add_words?set_id=3', json={'word_1': 'elo', 'word_2': 'benc'})

# requests.post(BASE + '/add_words?set_id=2', json={'word_1': 'sand', 'word_2': 'piasek'})

# response = requests.delete(BASE + '/delete_words?set_id=2&words_id=1')

# response = requests.patch(BASE + '/update_words?set_id=2&words_id=4', json={'word_1': 'ciasto', 'word_2': 'cake'})

# print(response.json())
