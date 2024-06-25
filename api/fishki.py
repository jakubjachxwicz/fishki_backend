from flask import Blueprint, request, jsonify
from db import create_set
from api.utils import expect


fishki_api_v1 = Blueprint('fishki_api_v1', 'fishki_api_v1', url_prefix='/api/v1/fishki')


@fishki_api_v1.route('/create_set', methods=['POST'])
def api_create_set():
    print('HI MUM!')

    post_data = request.get_json()
    try:
        set_id = expect(post_data.get('set_id'), int, 'set_id')
        name = expect(post_data.get('name'), str, 'name')
        lang_1 = expect(post_data.get('lang_1'), str, 'lang_1')
        lang_2 = expect(post_data.get('lang_2'), str, 'lang_2')
        print('data verified')

        create_set(set_id, name, lang_1, lang_2)
        return jsonify({'message': 'set added'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
