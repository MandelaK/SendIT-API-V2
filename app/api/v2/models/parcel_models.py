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
