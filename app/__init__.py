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

    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.category.views import category_view, category_specific_view
    app.add_url_rule('/category/', view_func=category_view)
    app.add_url_rule('/category/<int:category_id>', view_func=category_specific_view)

    from app.recipe.views import recipe_view, recipe_specific_view
    app.add_url_rule('/recipe/', view_func=recipe_view)
    app.add_url_rule('/recipe/<int:recipe_id>', view_func=recipe_specific_view)

    return app
