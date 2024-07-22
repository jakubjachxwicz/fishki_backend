import os
import configparser
from flask import Flask
from api.fishki import fishki_api_v1


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join('.ini')))


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['MONGO_URI'] = config['TEST']['DB_URI']
    app.register_blueprint(fishki_api_v1)

    app.run(host='0.0.0.0', debug=True)
