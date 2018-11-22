
from flask import Flask
# we import created blueprints to register them
from .api.v2 import version2
from db_config import create_tables, create_admin, delete_admin
from instance.config import app_config


def create_app(config_name):
    """This is our app factory from where we register our app and
    API version"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # we register the blueprint
    app.register_blueprint(version2)
    # register more blueprints in a similar manner
    create_tables()
    delete_admin()
    create_admin()

    return app
