from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import current_user


from models import db, User
from utils import admin_required


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", required=True, type=str, help="Email address is required"
    )
    parser.add_argument(
        "password", required=True, type=str, help="Password is required"
    )

    def post(self):
        data = self.parser.parse_args()

        # 1 Check if user with exists
        user = User.query.filter_by(email=data["email"]).first()

        if user is None:
            return {"message": "Invalid email or password"}, 403

        # 2 validate password is ok
        if check_password_hash(user.password, data["password"]):
            # 3. generate token
            access_token = create_access_token(
                identity=user.id, additional_claims={"role": user.role}
            )

            return {
                "message": "Login successful",
                "user": user.to_dict(),
                "access_token": access_token,
            }, 201
        else:
            return {"message": "Invalid email or password"}, 403


class SigninResource(Resource):
    # define the shape/body of signin
    parser = reqparse.RequestParser()
    parser.add_argument(
        "full_name", required=True, type=str, help="Full name is requried"
    )
    parser.add_argument(
        "email", required=True, type=str, help="Email address is required"
    )
    parser.add_argument(
        "password", required=True, type=str, help="Password is required"
    )

    def post(self):
        data = self.parser.parse_args()

        # 0. rate limiting ->

        # 1. ensure email is not taken
        email = User.query.filter_by(email=data["email"]).first()

        if email:
            return {"message": "Email address is already taken"}, 422

        # 2. encrypt password (argon2/bcrypt)
        hash = generate_password_hash(data["password"]).decode("utf-8")

        del data["password"]

        # 3. save user info
        user = User(**data, password=hash)

        db.session.add(user)
        db.session.commit()

        # 4. generate access token (JWT)
        access_token = create_access_token(
            identity=user.id, additional_claims={"role": user.role}
        )

        # 5. send welcome email

        return {
            "message": "Account created successfully",
            "access_token": access_token,
            "user": user.to_dict(),
        }, 201


class UsersResource(Resource):
    @admin_required()
    def get(self):
        # if current_user["role"] != "admin":
        #     return {"message": "Unauthorized request"}, 403

        data = User.query.all()

        result = []

        for user in data:
            result.append(user.to_dict())

        return result
