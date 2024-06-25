import requests

BASE = 'http://127.0.0.1:5000/api/v1/fishki'

response = requests.post(BASE + '/create_set', json={'set_id': 1, 'name': 'First set', 'lang_1': 'pl', 'lang_2': 'it'})
print(response.json())
