import psycopg2

from db_config import init_db
from werkzeug.security import check_password_hash


class Users():
    """This is the users model. All methods here will handle transactions with the users table"""

    def __init__(self):
        self.db = init_db()

    def save(self, first_name, last_name, email, password,
             phone):

        user_info = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "phone": phone
        }

        user_exists = self.get_user_by_email(email)
        if user_exists:
            return 409
        else:
            phone_exists = self.get_user_by_phone(phone)
            if phone_exists:
                return 409
        save_info = """INSERT INTO users
        (first_name, last_name, email, password, phone)
        VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s, %(phone)s)"""

        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Adding user to database ...")
            cursor.execute(save_info, user_info)
        except (Exception, psycopg2.Error) as error:
            print("Error while executing query:",
                  error, " Please try that again")
            return error, 400

        else:
            self.db.commit()
            print("User information added Successfully.")
            return 201

    def get_user_by_email(self, email):
        """This method returns the user if the exist in the database"""

        get_user = """SELECT * FROM users WHERE email = '{}'
        """.format(email)
        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Getting user {} ...".format(email))
            cursor.execute(get_user)
            user = cursor.fetchone()
            if not user:
                print("User {} not found.".format(email))
                return False
            else:
                print("User {} was found. ".format(email), user)
                return user
        except(Exception, psycopg2.Error) as error:
            print("Something went wrong: ", error)
            return error

    def get_user_by_phone(self, phone):
        """We use this to check if the phone number is already registered"""

        get_user = """SELECT * FROM users where phone = {}""".format(phone)
        try:
            cursor = self.db.cursor()
            print(
                "successfully created cursor. Getting user with phone number {} ...".format(phone))
            cursor.execute(get_user)
            user = cursor.fetchone()
            if not user:
                print("User with phone number {} not registered".format(phone))
                return False
            else:
                print("User with phone number {} is registered.".format(phone), user)
                return user
        except (Exception, psycopg2.Error) as error:
            print("Something went wrong: ", error)
            return error
