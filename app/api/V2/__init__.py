from flask import Blueprint
from flask_restful import Api

version2 = Blueprint("v2", __name__, url_prefix="/api/v2")
api_2 = Api(version2, catch_all_404s=True)
