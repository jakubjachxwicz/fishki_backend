import os
import configparser
from datetime import datetime, timedelta
from jwt import encode, decode, ExpiredSignatureError
from functools import wraps
from flask import request, jsonify

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
