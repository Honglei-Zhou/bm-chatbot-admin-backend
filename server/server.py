from flask import Flask
from server.config import db_string, mail_settings
import os


path = os.path.dirname( os.path.realpath(__file__) )

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'secret!'

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string', 'json']

app.config['JWT_TOKEN_LOCATION'] = ['headers']
# app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config.update(mail_settings)