import string
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from database import db_uri
from datetime import timedelta
import random

random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(2))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = "WsfHkVEfpsmoqNNBUNEkBu8Fi554tyzqUuWL5fLySV4"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

db = SQLAlchemy(app)
ma = Marshmallow(app)