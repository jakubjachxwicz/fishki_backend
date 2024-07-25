import os
import configparser
from datetime import datetime, timedelta
from jwt import encode, decode, ExpiredSignatureError
from functools import wraps
from flask import request, jsonify
from api.blueprint import fishki_api_v1
from db import get_user_by_email, create_user, update_username, update_email, get_user_by_id, \
    update_password, delete_user, delete_all_sets
from werkzeug.security import check_password_hash
from api.utils import expect
from email_validator import validate_email

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join('.ini')))


def create_token(user):
    expiration = datetime.utcnow() + timedelta(days=7)
    payload = {'user_id': str(user['user_id']), 'expiration': str(expiration)}

    return encode(payload, config['TEST']['SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    try:
        payload = decode(token, config['TEST']['SECRET_KEY'], algorithms='HS256')

        # print(payload)

        return payload['user_id']
    except ExpiredSignatureError:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authorization header is missing'}), 403

        parts = auth_header.split()
        if parts[0].lower() != 'bearer':
            return jsonify({'error': 'Authorization header must start with Bearer'}), 403
        if len(parts) == 1 or len(parts) > 2:
            return jsonify({'error': 'Authorization header must be a Bearer token'}), 403

        token = parts[1]
        try:
            user_id = decode_token(token)
            if not user_id:
                # print('Token is invalid or expired')
                return jsonify({'error': 'Token is invalid or expired'}), 403

            return f(user_id, *args, **kwargs)
        except Exception as e:
            # print(e)
            return jsonify({'error': 'Token is invalid or expired'}), 403

    return decorated


@fishki_api_v1.route('/register', methods=['POST'])
def register():
    body_data = request.get_json()

    # ZRÓB WALIDACJEEEEEEEEE
    # z expect() i jakieś walidacje email itp, długosci...
    if get_user_by_email(body_data.get('email')):
        return jsonify({'error': 'User already exist'}), 400

    user_id = create_user(body_data.get('username'), body_data.get('email'), body_data.get('password'))
    return jsonify({'message': 'User has been created', 'user_id': user_id}), 201


@fishki_api_v1.route('/login', methods=['POST'])
def login():
    body_data = request.get_json()

    #TU TEZ WALIDACJA JAK WYZEJ EJST DO ZROBIENIA
    user = get_user_by_email(body_data.get('email'))
    if user and check_password_hash(user['password'], body_data.get('password')):
        token = create_token(user)
        return jsonify({'message': 'Login successful', 'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401


@fishki_api_v1.route('/verify_token', methods=['GET'])
@token_required
def verify_token(user_id):
    # print(user_id)
    return jsonify({'message': 'Token is valid'}), 200


@fishki_api_v1.route('/update_username', methods=['PATCH'])
@token_required
def api_update_username(user_id):
    body_data = request.get_json()
    try:
        new_username = expect(body_data.get('username'), str, 'new_username')
        if len(new_username) > 20:
            return jsonify({'error': 'Username is too long'}), 400

        res = update_username(int(user_id), new_username)
        if res.raw_result['ok'] == 1.0:
            return jsonify({'message': 'Username updated'}), 200

        return jsonify({'error': 'Couldn\'t change the username'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/update_email', methods=['PATCH'])
@token_required
def api_update_email(user_id):
    body_data = request.get_json()
    try:
        new_email = expect(body_data.get('email'), str, 'new_email')
        email = validate_email(new_email, check_deliverability=False)
        res = update_email(int(user_id), email.normalized)

        if res.raw_result['ok'] == 1.0:
            return jsonify({'message': 'Email updated'}), 200

        return jsonify({'error': 'Couldn\'t update email'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/update_password', methods=['PATCH'])
@token_required
def api_update_password(user_id):
    body_data = request.get_json()
    try:
        old_password = expect(body_data.get('old_password'), str, 'old_password')
        new_password = expect(body_data.get('new_password'), str, 'new_password')

        user = get_user_by_id(int(user_id))
        if not check_password_hash(user['password'], old_password):
            return jsonify({'error': 'Old password is incorrect'}), 400

        res = update_password(int(user_id), new_password)

        if res.raw_result['ok'] == 1.0:
            return jsonify({'message': 'Email updated'}), 200

        return jsonify({'error': 'Couldn\'t update password'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/get_user_data', methods=['GET'])
@token_required
def api_get_user_data(user_id):
    try:
        res = get_user_by_id(int(user_id))
        if res:
            del res['_id']
            return jsonify(res), 200

        return jsonify({'error': 'Couldn\'t retrieve user data'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@fishki_api_v1.route('/delete_user', methods=['DELETE'])
@token_required
def api_delete_user(user_id):
    try:
        res1 = delete_all_sets(int(user_id))
        if res1.raw_result['ok'] == 1.0:
            res2 = delete_user(int(user_id))
            if res2.raw_result['ok'] == 1.0:
                return jsonify({'message': 'User deleted'}), 200

        return jsonify({'error': 'Couldn\'t delete user'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400
