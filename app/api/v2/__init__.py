from flask import Blueprint
from flask_restful import Api

from app.api.v2.views.user_views import SignupView, LoginView
from app.api.v2.views.parcel_views import ParcelCreate

version2 = Blueprint("v2", __name__, url_prefix="/api/v2")
api2 = Api(version2, catch_all_404s=True)


api2.add_resource(SignupView, "/auth/signup")
api2.add_resource(LoginView, "/auth/login")
api2.add_resource(ParcelCreate, "/users/parcels")
