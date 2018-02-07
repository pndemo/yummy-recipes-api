""" Initial application specifications """

from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flasgger import Swagger

# pylint: disable=C0103

db = SQLAlchemy()

def create_app(config_name):
    """ Function for creating application depending on configuration """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    app.config['SWAGGER'] = {
        "swagger": "2.0",
        "title": "Yummy Recipes API",
        "info": {
            "title": "Yummy Recipes API",
            "description": "This app enables you to access Yummy Recipes resources, a platform \
                    for users to keep track of their awesome recipes and share with others if \
                    they so wish. The API functionalities include: creation of new user \
                    accounts, user login, password reset, creation of new recipe categories, \
                    viewing of recipe categories, updating of recipe categories, deletion of \
                    recipe categories, creation of new recipes, viewing of recipes, updating of \
                    recipes and deletion of recipes.",
            "contact": {
                "responsibleOrganization": "Yummy Recipes Inc.",
                "responsibleDeveloper": "Paul Ndemo Oroko",
                "url": "https://github.com/pndemo/yummy-recipes-api",
            }
        },
        "schemes": ["http", "https"],
        'securityDefinitions': {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
    }

    Swagger(app)

    db.init_app(app)

    def index():
        """ Yummy Recipes API home page """
        return redirect('/apidocs')

    from app.v1.views import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.v1.views.category_views import category_view, category_specific_view, \
            category_search_view
    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/api/v1/category/', view_func=category_view)
    app.add_url_rule('/api/v1/category/<int:category_id>', view_func=category_specific_view)
    app.add_url_rule('/api/v1/category/search', view_func=category_search_view)

    from app.v1.views.recipe_views import recipe_view, recipe_specific_view, recipe_search_view
    app.add_url_rule('/api/v1/recipe/<int:category_id>/', view_func=recipe_view)
    app.add_url_rule('/api/v1/recipe/<int:category_id>/<int:recipe_id>', view_func= \
            recipe_specific_view)
    app.add_url_rule('/api/v1/recipe/<int:category_id>/search', view_func=recipe_search_view)

    return app
