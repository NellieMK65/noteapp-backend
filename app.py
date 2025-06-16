from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS

from models import db
from resources.users import SigninResource

app = Flask(__name__)

# setup cors
CORS(app)

# setup flask-restful
api = Api(app)

# configure our app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///note.db"

app.config["SQLALCHEMY_ECHO"] = True

migrate = Migrate(app, db)

db.init_app(app)


api.add_resource(SigninResource, "/signin")
