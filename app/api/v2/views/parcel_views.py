from flask_restful import Resource
from flask_restful.reqparse import RequestParser as R
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.v2.models.parcel_models import Parcels
from app.api.v2.UTILS import helpers


class ParcelCreate(Resource, Parcels):
    """This class contains methods that will be used to create parcel orders by users"""

    def __init__(self):
        self.parcel = Parcels()
        self.inspect_parcel_details = R()
        self.inspect_parcel_details.add_argument(
            "parcel_name", help="Please give your parcel a name", required=True)
        self.inspect_parcel_details.add_argument(
            "recipient_name", help="Provide the name of the recipient", required=True)
        self.inspect_parcel_details.add_argument(
            "pickup_location", help="Please enter the pickup location", required=True)
        self.inspect_parcel_details.add_argument(
            "destination", help="Please enter the destination", required=True)
        self.inspect_parcel_details.add_argument(
            "weight", help="Please enter the weight", required=True)

    @jwt_required
    def post(self):

        user_data = get_jwt_identity()
        if user_data["is_admin"] is True:
            return 403

        parcel_details = self.inspect_parcel_details.parse_args()

        parcel_name = parcel_details.get("parcel_name")
        recipient_name = parcel_details.get("recipient_name")
        pickup_location = parcel_details.get("pickup_location")
        destination = parcel_details.get("destination")
        weight = parcel_details.get("weight")

        if not helpers.validate_string(parcel_name):
            return {"Error": "Please enter valid parcel name"}, 400
        if not helpers.validate_string(recipient_name):
            return {"Error": "Please enter valid recipient name"}, 400
        if not helpers.validate_string(pickup_location):
            return {"Error": "Please enter valid pickup location"}, 400
        if not helpers.validate_string(destination):
            return {"Error": "Please enter valid destination"}, 400
        if not helpers.validate_int(weight):
            return {"Error": "Please enter postive weight in integers"}, 400

        save_parcel = self.parcel.create_parcel(
            parcel_name, recipient_name, pickup_location, destination, weight)

        if save_parcel == 201:
            return {"Success": "Your parcel order has been saved"}, 201
        else:
            return {"Something went wrong": save_parcel}, 400
