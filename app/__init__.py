""" Initial application specifications """

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()

def create_app(config_name):
    """Function for creating application depending on configuration"""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    from app.v1.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.v1.category.category_views import category_view, category_specific_view, \
            category_search_view
    app.add_url_rule('/api/v1/category/', view_func=category_view)
    app.add_url_rule('/api/v1/category/<int:category_id>', view_func=category_specific_view)
    app.add_url_rule('/api/v1/category/search', view_func=category_search_view)

    from app.v1.recipe.recipe_views import recipe_view, recipe_specific_view, recipe_search_view
    app.add_url_rule('/api/v1/recipe/<int:category_id>/', view_func=recipe_view)
    app.add_url_rule('/api/v1/recipe/<int:category_id>/<int:recipe_id>', view_func= \
            recipe_specific_view)
    app.add_url_rule('/api/v1/recipe/<int:category_id>/search', view_func=recipe_search_view)

    return app
