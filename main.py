import os
import configparser
from flask import Flask
from flask_restful import Api


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join('.ini')))


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['MONGO_URI'] = config['TEST']['DB_URI']
    api = Api(app)

    app.run(debug=True)
