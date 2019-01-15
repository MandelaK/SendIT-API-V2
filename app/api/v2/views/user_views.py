import datetime

from flask_restful import Resource
from flask_restful.reqparse import RequestParser as R
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from validate_email import validate_email

from app.api.v2.models.user_models import Users
from app.api.v2.UTILS import helpers


class SignupView(Resource, Users):
    """Methods created here define how user requests are handled before being sent to the models"""

    def __init__(self):
        self.users = Users()
        self.inspect_user_data = R()
        self.inspect_user_data.add_argument(
            "first_name", help="Please enter first name", required=True)
        self.inspect_user_data.add_argument(
            "last_name", help="Please enter last name", required=True)
        self.inspect_user_data.add_argument(
            "email", help="Please enter email", required=True)
        self.inspect_user_data.add_argument(
            "password", help="Please enter password", required=True)
        self.inspect_user_data.add_argument(
            "confirm_password", help="Please confrim your password", required=True)
        self.inspect_user_data.add_argument("phone", required=False)

    def post(self):
        """When user wants to create new account we validate their data
        first before we can add them to the database"""
        user_data = self.inspect_user_data.parse_args()

        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        email = user_data.get("email")
        password = user_data.get("password")
        confirm_password = user_data.get("confirm_password")
        phone = user_data.get("phone")

        if not helpers.validate_string(first_name):
            return {"Error": "Please enter valid first name"}, 400
        if not helpers.validate_string(last_name):
            return {"Error": "Please enter valid last name"}, 400
        if not validate_email(email):
            return {"Error": "Please enter valid email adress"}, 400
        if len(password) < 6:
            return {"Error": "Password must be 6 or more characters"}, 400
        if not helpers.validate_string(password):
            return {"Error": "Password must contain digits"}, 400
        if password != confirm_password:
            return {"Error": "Passwords don't match"}, 400
        if not helpers.validate_phone_number(phone):
            return {"Error": "Please enter valid phone number without any symbols",
                    "current length": len(phone)}, 400

        psw_hash = generate_password_hash(password)

        saving = self.users.save(first_name, last_name, email, psw_hash, phone)

        if saving == 201:
            return {"Success": "Succesfully created account for {}".format(email)}, 201
        elif saving == 409:
            return {"Error": "User already exists"}, 409
        elif saving == 400:
            return {"Error": "Could not create account. Please try again"}, 400


class LoginView(Resource, Users):
    """This class contains methods that handle requests for user login"""

    def __init__(self):
        self.user = Users()
        self.inspect_user_login = R()
        self.inspect_user_login.add_argument(
            "email", help="Please enter email adress", required=True)
        self.inspect_user_login.add_argument(
            "password", help="Please enter password", required=True)

    def post(self):
        """When the user submits login information, it is processed by this veiw before being
        submitted to the models"""
        login_info = self.inspect_user_login.parse_args()
        email = login_info.get("email")
        password = login_info.get("password")

        if not validate_email(email):
            return {"Error": "Incorrect email address"}, 422
        if not helpers.validate_string(password):
            return {"Error": "Incorrect password"}, 401

        user_info = self.user.log_in(email, password)
        if user_info == 404:
            return {"Error": "User does not exist"}, 404
        elif user_info == 401:
            return {"Error": "Incorrect credentials. Please try again"}, 401
        else:
            user_id = user_info[0]
            email = user_info[3]
            is_admin = user_info[6]
            user_dict = dict(
                user_id=user_id,
                email=email,
                is_admin=is_admin)

            token_expires = datetime.timedelta(minutes=600)
            token = create_access_token(
                identity=user_dict, expires_delta=token_expires)
            if is_admin:
                return {"Success": "You are logged in as admin.",
                        "email": email,
                        "token": token,
                        "admin": True}

            return {"Success": "You are logged in as {}.".format(email),
                    "token": token,
                    "email": email,
                    "admin": False}, 201
