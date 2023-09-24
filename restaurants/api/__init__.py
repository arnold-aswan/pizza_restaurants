from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurants.db"
app.config[" SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

from api import routes