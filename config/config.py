import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from database.database import db_uri
from datetime import timedelta
import random


random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(2))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'


db = SQLAlchemy(app)
ma = Marshmallow(app)

admin = Admin(app, name='Ecologic', template_mode='bootstrap3')