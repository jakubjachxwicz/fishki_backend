import requests

BASE = 'http://127.0.0.1:5000/api/v1/fishki'

response = requests.patch(BASE + '/update_password', json={'old_password': 'Kanapka123', 'new_password': 'rabarbar'})
