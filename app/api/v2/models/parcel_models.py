import psycopg2
from db_config import init_db
from flask_jwt_extended import jwt_required, get_jwt_identity


class Parcels():
    """The methods defined in this class represent methods that users
    will use to manipulate parcels in the database"""

    def __init__(self):
        self.db = init_db()

    def create_parcel(self, parcel_name, recipient_name, pickup_location,
                      destination, weight):
        """This method handles requests for creating parcel delivery orders"""

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

    @jwt_required
    def get_all_parcels(self):
        """This will be called if the admin wishes to see all parcels
        in the database"""

        user_data = get_jwt_identity()
        if user_data["is_admin"] is True:
            admin = True
            admin_get_all = """
                SELECT * FROM parcels
                ORDER BY parcel_id"""
        else:
            admin = False
            user_get_all = """
            SELECT * FROM parcels
            WHERE sender_email = '{}'
            ORDER BY parcel_id
            """.format(user_data["email"])

        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Getting all parcels ...")

            if admin is True:
                cursor.execute(admin_get_all)
            else:
                cursor.execute(user_get_all)

            data = cursor.fetchall()
            if data == []:
                return 404
            res = []

            for parcel, parcels in enumerate(data):
                parcel_id, parcel_name, sender_email, recipient_name, pickup_location, current_location, destination, weight, price, status = parcels
                structured_response = dict(
                    parcel_id=parcel_id,
                    parcel_name=parcel_name,
                    sender_email=sender_email,
                    recipient_name=recipient_name,
                    pickup_location=pickup_location,
                    current_location=current_location,
                    destination=destination,
                    weight=int(weight),
                    price=int(price),
                    status=status)
                res.append(structured_response)
            return res

        except (Exception, psycopg2.Error) as error:
            print("Could not get any parcels from database: ", error)
            return error

    def change_status(self, parcel_id, status):
        """This method handles requests to change the status of an order"""
        parcel = self.get_parcel_by_id(parcel_id)

        if not parcel:
            return 404
        elif parcel[9] == "delivered" or parcel[9] == "cancelled":
            return 400
        else:
            change_status = """
            UPDATE parcels SET status = '{}' WHERE parcel_id = {}""".format(status, parcel_id)
        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Changing the status of parcel number {} ...".format(
                parcel_id))
            cursor.execute(change_status)
            self.db.commit()
            count = cursor.rowcount
            print("Successfully changed the status parcel {}. {} rows affected.".format(
                parcel_id, count))
            return 204
        except (Exception, psycopg2.Error) as error:
            print("Could not change the status of the order: ", error)
            return error, 400

    def change_location(self, parcel_id, current_location):
        """This method handles requests to change the location of a delivery in transit"""

        parcel = self.get_parcel_by_id(parcel_id)

        if not parcel:
            return 404
        elif parcel[9] != "transit":
            return 400
        else:
            update_location = """
            UPDATE parcels SET current_location = '{}'
            WHERE parcel_id = {}""".format(current_location, parcel_id)

        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Updating current location for parcel \
                number {} ...".format(parcel_id))
            cursor.execute(update_location)
            self.db.commit()
            print("Location successfully changed")
            return 204
        except (Exception, psycopg2.Error) as error:
            print("Could not change destinaion of parcel: ", error)
            return error

    @jwt_required
    def cancel_parcel(self, parcel_id):
        """User can only cancel orders they create so long as they are not yet
        'delivered'"""
        user_data = get_jwt_identity()
        get_parcel = self.get_parcel_by_id(parcel_id)

        if get_parcel is False:
            return 404
        elif user_data["email"] != get_parcel[2]:
            return 401
        elif get_parcel[9] == "cancelled" or get_parcel[9] == "delivered":
            return 400
        else:
            cancel_query = """UPDATE parcels
            SET status = 'cancelled' WHERE parcel_id = {}""".format(parcel_id)

        try:
            cursor = self.db.cursor()
            print("Successfully created cursor. Cancelling parcel number {} ...".format(
                parcel_id))
            cursor.execute(cancel_query)
            self.db.commit()
            count = cursor.rowcount
            print("Successfully changed the status parcel {}. {} rows affected.".format(
                parcel_id, count))
            return 204
        except (Exception, psycopg2.Error) as error:
            print("Could not change the status of the parcel: ", error)
            return error
