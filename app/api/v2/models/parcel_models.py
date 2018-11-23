import psycopg2
from db_config import init_db
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.v2.models.user_models import Users


class Parcels():
    """The methods defined in this class represent methods that users
    will use to manipulate parcels in the database"""

    def __init__(self):
        self.db = init_db()

    def create_parcel(self, parcel_name, recipient_name, pickup_location,
                      destination, weight):
        """This method handles requests for creating parcel delivery orders"""
        # import pdb
        # pdb.set_trace()

        user_data = get_jwt_identity()
        self.parcel_name = parcel_name
        self.sender_email = user_data["email"]
        self.recipient_name = recipient_name
        self.destination = destination
        self.pickup_location = pickup_location
        self.current_location = pickup_location
        self.weight = int(weight)
        self.price = int(weight) * 3
        self.status = "pending"

        parcel_info = {
            "parcel_name": parcel_name,
            "sender_email": self.sender_email,
            "recipient_name": recipient_name,
            "pickup_location": pickup_location,
            "current_location": self.current_location,
            "destination": destination,
            "weight": int(weight),
            "price": int(self.price),
            "status": self.status
        }

        save_parcel = """
        INSERT INTO parcels (parcel_name, sender_email, recipient_name,
        pickup_location, current_location, destination, weight, price, status)
        VALUES (%(parcel_name)s, %(sender_email)s, %(recipient_name)s,
        %(pickup_location)s, %(current_location)s, %(destination)s, %(weight)s,
        %(price)s, %(status)s)"""
        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Saving parcel to database...")
            cursor.execute(save_parcel, parcel_info)
        except (Exception, psycopg2.Error) as error:
            print("Could not save the parcel to database: ", error)
            return error
        else:
            self.db.commit()
            print("Successfully saved the order to database")
            return 201

    def change_destination(self, parcel_id, destination):
        """This method will handle requests to the database to change the destination
        of a parcel delivery order."""

        user_data = get_jwt_identity()
        parcel = self.get_parcel_by_id(parcel_id)
        if not parcel:
            return 404
        elif parcel[2] != user_data["email"]:
            return 401
        elif parcel[9] != "pending":
            return 400
        else:
            update_destination = """UPDATE parcels SET destination = '{}'
            WHERE parcel_id = {}""".format(destination, parcel_id)
        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Updating destination for parcel number {} ...".format(
                parcel_id))
            cursor.execute(update_destination)
            self.db.commit()
            count = cursor.rowcount
            print("Destination successfully changed for parcel {}. {} rows affected".format(
                parcel_id, count))
            return 204
        except (Exception, psycopg2.Error) as error:
            print("Error. Could not update destination of parcel: ", error)
            return error

    def get_parcel_by_id(self, parcel_id):
        """We have to validate a parcel exists before we can begin to make
        changes on it."""

        get_parcel = """SELECT * FROM parcels WHERE parcel_id = {}
        """.format(parcel_id)
        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Getting parcel {} ...".format(parcel_id))
            cursor.execute(get_parcel)
            parc = cursor.fetchone()
            if not parc:
                return False
            else:
                return parc
        except (Exception, psycopg2.Error) as error:
            print ("Could not get parcel {}... ".format(parcel_id), error)
            return error
