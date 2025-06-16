from flask_restful import Resource, reqparse
from models import db, User


class SigninResource(Resource):
    # define the shape/body of signin
    parser = reqparse.RequestParser()
    parser.add_argument(
        "full_name", required=True, type=str, help="Full name is requried"
    )
    parser.add_argument(
        "email", required=True, type=str, help="Email address is required"
    )
    # parser.add_argument("password", required=True, type=str, help="Password is required")

    def post(self):
        data = self.parser.parse_args()

        # 0. rate limiting ->

        # 1. ensure email is not taken
        email = User.query.filter_by(email=data["email"]).first()

        if email:
            return {"message": "Email address is already taken"}, 422

        # 2. encrypt password (argon2/bcrypt)

        # 3. save user info
        user = User(**data)

        db.session.add(user)
        db.session.commit()

        # 4. generate access token (JWT)

        # 5. send welcome email

        return {"message": "Account created successfully"}, 201
