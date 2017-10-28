""" Initial application specifications """

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from config import app_config

# pylint: disable=C0103

db = SQLAlchemy()

def create_app(config_name):
    """Function for creating application depending on configuration"""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    return app
