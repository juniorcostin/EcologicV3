from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from database import db_uri
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = 'WsfHkVEfpsmoqNNBUNEkBu8Fi554tyzqUuWL5fLySV4'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

login_manager = LoginManager(app)
db = SQLAlchemy(app)