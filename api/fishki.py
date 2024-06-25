from flask import Blueprint, request, jsonify
from db import create_set, add_words, count_sets, set_exists
from api.utils import expect


fishki_api_v1 = Blueprint('fishki_api_v1', 'fishki_api_v1', url_prefix='/api/v1/fishki')


@fishki_api_v1.route('/create_set', methods=['POST'])
def api_create_set():
    post_data = request.get_json()
    try:
        count = count_sets()
        while set_exists(count):
            count += 1
        set_id = count
        name = expect(post_data.get('name'), str, 'name')
        lang_1 = expect(post_data.get('lang_1'), str, 'lang_1')
        lang_2 = expect(post_data.get('lang_2'), str, 'lang_2')

        create_set(set_id, name, lang_1, lang_2)
        return jsonify({'message': 'Set added...'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/add_words', methods=['POST'])
def api_add_words():
    post_data = request.get_json()
    try:
        set_id = expect(post_data.get('set_id'), int, 'set_id')
        w1 = expect(post_data.get('word_1'), str, 'word_1')
        w2 = expect(post_data.get('word_2'), str, 'word_2')
        words = [w1, w2]

        add_words(set_id, words)
        return jsonify({'message': f'Words added to set {set_id}...'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
