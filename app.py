import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from models import db, User
from resources.users import SigninResource, LoginResource, UsersResource
from resources.payment import (
    PaymentResource,
    PaymentCallbackResource,
    CheckPaymentResource,
)

# load environment variables
load_dotenv()

app = Flask(__name__)

# setup cors
CORS(app)

# setup flask-restful
api = Api(app)

# configure our app
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

app.config["SQLALCHEMY_ECHO"] = True

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

app.config["BUNDLE_ERRORS"] = True

jwt = JWTManager(app)

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

db.init_app(app)


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     user = User.query.filter_by(id=identity).one_or_none()

#     if user is None:
#         return {}
#     else:
#         return user.to_dict()


class Index(Resource):
    def get(self):
        return {"message": "Welcome to the notted api"}


api.add_resource(Index, "/")
api.add_resource(SigninResource, "/signin")
api.add_resource(LoginResource, "/login")
api.add_resource(UsersResource, "/users")
api.add_resource(PaymentResource, "/payments")
api.add_resource(PaymentCallbackResource, "/payments/callback")
api.add_resource(CheckPaymentResource, "/payments/check/<string:checkout_request_id>")

if __name__ == "__main__":
    app.run(port=5555)
