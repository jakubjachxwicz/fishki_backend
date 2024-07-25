from flask import request, jsonify
from db import create_set, add_words, count_sets, set_exists, last_words_id, update_set, \
    get_set, update_words, delete_set_by_id, delete_words_by_id, delete_all_words, \
    get_all_sets, get_user_id
from api.auth import token_required
from api.utils import expect
from api.blueprint import fishki_api_v1


@fishki_api_v1.route('/get_set', methods=['GET'])
@token_required
def api_get_set(user_id):
    try:
        set_id = expect(int(request.args.get('set_id')), int, 'set_id')
        if not set_exists(set_id):
            return jsonify({'error': f'Set with id {set_id} doesn\'t exist...'}), 404

        res = get_set(set_id)
        del res['_id']

        if res.get('user_id') != int(user_id):
            return jsonify({'error': 'Invalid credentials'}), 403

        return jsonify(res)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/get_words', methods=['GET'])
@token_required
def api_get_words(user_id):
    try:
        set_id = expect(int(request.args.get('set_id')), int, 'set_id')
        if not set_exists(set_id):
            return jsonify({'error': f'Set with id {set_id} doesn\'t exist...'}), 404

        res = get_set(set_id)

        if res.get('user_id') != int(user_id):
            return jsonify({'error': 'Invalid credentials'}), 403

        return jsonify(res['words'])

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/get_all_sets', methods=['GET'])
@token_required
def api_get_all_sets(user_id):
    result = get_all_sets(int(user_id))
    return jsonify(result)


@fishki_api_v1.route('/create_set', methods=['POST'])
@token_required
def api_create_set(user_id):
    post_data = request.get_json()
    try:
        count = count_sets()
        while set_exists(count):
            count += 1
        name = expect(post_data.get('name'), str, 'name')
        lang_1 = expect(post_data.get('lang_1'), str, 'lang_1')
        lang_2 = expect(post_data.get('lang_2'), str, 'lang_2')

        create_set(count, int(user_id), name, lang_1, lang_2)
        return jsonify({'message': 'Set added...'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/update_set', methods=['PATCH'])
@token_required
def api_update_set(user_id):
    body_data = request.get_json()
    try:
        set_id = expect(int(request.args.get('set_id')), int, 'set_id')
        if not set_exists(set_id):
            return jsonify({'error': f'Set with id {set_id} doesn\'t exist...'}), 404
        set_data = get_set(set_id)

        if get_user_id(set_id) != int(user_id):
            return jsonify({'error': 'Invalid credentials'}), 403

        if not body_data.get('name'):
            name = set_data['name']
        else:
            name = expect(body_data.get('name'), str, 'name')

        if not body_data.get('lang_1'):
            lang_1 = set_data['lang_1']
        else:
            lang_1 = expect(body_data.get('lang_1'), str, 'lang_1')

        if not body_data.get('lang_2'):
            lang_2 = set_data['lang_2']
        else:
            lang_2 = expect(body_data.get('lang_2'), str, 'lang_2')

        update_set(set_id, name, lang_1, lang_2)
        return jsonify({'message': f'Set with id {set_id} updated...'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/delete_set', methods=['DELETE'])
@token_required
def api_delete_set(user_id):
    try:
        set_id = expect(int(request.args.get('set_id')), int, 'set_id')
        if not set_exists(set_id):
            return jsonify({'error': f'Set with id {set_id} doesn\'t exist...'}), 404

        if get_user_id(set_id) != int(user_id):
            return jsonify({'error': 'Invalid credentials'}), 403

        delete_set_by_id(set_id)
        return jsonify({'message': 'Set has been deleted...'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/add_words', methods=['POST'])
@token_required
def api_add_words(user_id):
    post_data = request.get_json()
    try:
        set_id = expect(int(request.args.get('set_id')), int, 'set_id')
        if not set_exists(set_id):
            return jsonify({'error': f'Set with id {set_id} doesn\'t exist...'}), 404
        w1 = expect(post_data.get('word_1'), str, 'word_1')
        w2 = expect(post_data.get('word_2'), str, 'word_2')

        if get_user_id(set_id) != int(user_id):
            return jsonify({'error': 'Invalid credentials'}), 403

        id = last_words_id(set_id) + 1
        words = {'words_id': id, 'word_1': w1, 'word_2': w2}

        add_words(set_id, words)
        return jsonify({'message': f'Words added to set {set_id}...'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/update_words', methods=['PATCH'])
@token_required
def api_update_words(user_id):
    body_data = request.get_json()
    try:
        set_id = expect(int(request.args.get('set_id')), int, 'set_id')
        if not set_exists(set_id):
            return jsonify({'error': f'Set with id {set_id} doesn\'t exist...'}), 404

        words_id = expect(int(request.args.get('words_id')), int, 'words_id')
        w1 = expect(body_data.get('word_1'), str, 'word_1')
        w2 = expect(body_data.get('word_2'), str, 'word_2')

        if get_user_id(set_id) != int(user_id):
            return jsonify({'error': 'Invalid credentials'}), 403

        update_words(set_id, {'words_id': words_id, 'word_1': w1, 'word_2': w2})
        return jsonify({'message': 'Words updated...'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/delete_words', methods=['DELETE'])
@token_required
def api_delete_words(user_id):
    try:
        set_id = expect(int(request.args.get('set_id')), int, 'set_id')
        if not set_exists(set_id):
            return jsonify({'error': f'Set with id {set_id} doesn\'t exist...'}), 404
        words_id = expect(int(request.args.get('words_id')), int, 'words_id')

        if get_user_id(set_id) != int(user_id):
            return jsonify({'error': 'Invalid credentials'}), 403

        delete_words_by_id(set_id, words_id)
        return jsonify({'message': 'Words deleted...'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/delete_all_words', methods=['DELETE'])
def api_delete_all_words():
    body_data = request.get_json()
    try:
        set_id = expect(body_data.get('set_id'), int, 'set_id')
        if not set_exists(set_id):
            return jsonify({'error': f'Set with id {set_id} doesn\'t exist...'}), 404

        delete_all_words(set_id)
        return jsonify({'message': 'Words from set deleted'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
