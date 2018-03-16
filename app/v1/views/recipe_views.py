""" Recipe view for creating, viewing, updating and deleting recipes """

from flask import jsonify, request, url_for
from flask_restful import Resource, reqparse
from sqlalchemy import exc
from app.v1.models.category_models import Category
from app.v1.models.recipe_models import Recipe
from app.v1.validators import data_validator
from app.v1.validators.recipe_validators import validate_recipe_name, validate_ingredients, \
        validate_directions
from app.v1.utils.decorators import authenticate
from app.v1.utils.paginator import get_paginated_results

# pylint: disable=C0103
# pylint: disable=W0703
# pylint: disable=W0613

class RecipeView(Resource):
    """Allows for creation and listing of recipe categories."""

    method_decorators = [authenticate]

    parser = reqparse.RequestParser()
    parser.add_argument('recipe_name', type=str, help='Recipes\'s recipe name')
    parser.add_argument('ingredients', type=str, help='Recipes\'s ingredients')
    parser.add_argument('directions', type=str, help='Recipes\'s directions')

    def post(self, access_token, user, category_id):
        """
        Process POST request
        ---
        tags:
          - Recipe
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of recipe category
            type: int
          - in: body
            name: body
            required: true
            description: Recipe's name, ingredients, directions and category_id
            type: string
            schema:
              properties:
                recipe_name:
                  type: string
                  default: Espresso Esiri
                ingredients:
                  type: string
                  default: 1) 1 tbsp plus 1 or 2 tsp (20-25 ml) Espresso, 2) 2 \
tbsp (30 ml) Benedictine, 3) Approx. 3 tbsp (40 ml) fresh heavy cream, 4) Unsweetened \
cocoa powder, 5) Ice cubes
                directions:
                  type: string
                  default: 1) Prepare the Espresso in a small cup. 2) Fill the mixing \
glass 3/4 full with ice cubes. Add the Benedictine and the Espresso. Cool, mixing the \
ingredients with the mixing spoon. 3) Pour into the glass, filtering the ice with a strainer. \
4) Shake the cream, which should be very cold, in the mini shaker until it becomes quite thick. \
5) Rest the cream on the surface of the cocktail, making it run down the back of the mixing spoon. \
6) Garnish with a light dusting of cocoa, and serve.
                category_id:
                  type: int
                  default: 1
        responses:
          201:
            description: A new recipe created successfully
          400:
            description: Data validation failed
          404:
            description: Invalid recipe category id
          500:
            description: Database could not be accessed
        """

        args = self.parser.parse_args()

        messages = {}
        messages['recipe_name_message'] = validate_recipe_name(args.recipe_name.strip(), category_id)
        messages['ingredients_message'] = validate_ingredients(args.ingredients)
        messages['directions_message'] = validate_directions(args.directions)

        if not data_validator(messages):
            return jsonify(messages), 400

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                recipe = Recipe(recipe_name=args.recipe_name, ingredients=args.ingredients, \
                        directions=args.directions, category_id=category_id)
                recipe.save()
                response = jsonify({
                    'id': recipe.id,
                    'recipe_name': recipe.recipe_name,
                    'ingredients': recipe.ingredients,
                    'directions': recipe.directions,
                    'category_id': recipe.category_id,
                    'date_created': recipe.date_created,
                    'date_modified': recipe.date_modified
                })
                response.status_code = 201
            else:
                response = jsonify({'message': 'Sorry, recipe category could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

    def get(self, access_token, user, category_id):
        """
        Process GET request
        ---
        tags:
          - Recipe
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of recipe(s) category
            type: int
          - in: query
            name: page
            description: Page number to display
          - in: query
            name: limit
            description: Number of recipes to display per page
        responses:
          200:
            description: Categories retrieved successfully
          400:
            description: Non-integer page and limit values submitted
          404:
            description: Invalid recipe category id
          500:
            description: Database could not be accessed
        """

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                recipes = Recipe.query.filter_by(category_id=category.id).all()
                paginated = get_paginated_results(request, recipes, url_for('category_view') + '?')
                if paginated['is_good_query']:
                    results = []
                    for recipe in paginated['results']:
                        obj = {
                            'id': recipe.id,
                            'recipe_name': recipe.recipe_name,
                            'ingredients': recipe.ingredients,
                            'directions': recipe.directions,
                            'category_id': recipe.category_id,
                            'date_created': recipe.date_created,
                            'date_modified': recipe.date_modified
                        }
                        results.append(obj)
                    response = jsonify({
                        'results': results,
                        'previous_link': paginated['previous_link'],
                        'next_link': paginated['next_link']
                        })
                    response.status_code = 200
                else:
                    response = jsonify({'message': 'Please enter valid page and limit values.'})
                    response.status_code = 400
            else:
                response = jsonify({'message': 'Sorry, recipe category could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

class RecipeSpecificView(Resource):
    """Allows for viewing, updating and and deletion of specific recipe category."""

    method_decorators = [authenticate]

    parser = reqparse.RequestParser()
    parser.add_argument('recipe_name', type=str, help='Recipes\'s recipe name')
    parser.add_argument('ingredients', type=str, help='Recipes\'s ingredients')
    parser.add_argument('directions', type=str, help='Recipes\'s directions')

    def get(self, access_token, user, category_id, recipe_id):
        """
        Process GET request
        ---
        tags:
          - Recipe
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of recipe category
            type: int
          - in: path
            name: recipe_id
            required: true
            description: The id of recipe requested
            type: int
        responses:
          200:
            description: Recipe retrieved successfully
          404:
            description: Category/recipe with id could not be found
          500:
            description: Database could not be accessed
        """

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                recipe = Recipe.query.filter_by(id=recipe_id, category_id=category.id).first()
                if recipe:
                    response = jsonify({
                        'id': recipe.id,
                        'recipe_name': recipe.recipe_name,
                        'ingredients': recipe.ingredients,
                        'directions': recipe.directions,
                        'category_id': recipe.category_id,
                        'date_created': recipe.date_created,
                        'date_modified': recipe.date_modified
                    })
                    response.status_code = 200
                else:
                    response = jsonify({'message': 'Sorry, recipe could not be found.'})
                    response.status_code = 404
            else:
                response = jsonify({'message': 'Sorry, recipe category could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

    def put(self, access_token, user, category_id, recipe_id):
        """
        Process PUT request
        ---
        tags:
          - Recipe
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of recipe category
            type: int
          - in: path
            name: recipe_id
            required: true
            description: The id of recipe requested
            type: int
          - in: body
            name: body
            required: true
            description: Recipe's name, ingredients and directions
            type: string
            schema:
              properties:
                recipe_name:
                  type: string
                  default: Apple Cinnamon White Cake
                ingredients:
                  type: string
                  default: 1) 1 teaspoon ground cinnamon 2) 2/3 cup white sugar \
3) 1/2 cup butter, softened 4) 2 eggs 5) 1 1/2 teaspoons vanilla extract 6) 1 1/2 \
cups all-purpose flour 7) 1 3/4 teaspoons baking powder 8) 1/2 cup milk 9) 1 apple, \
peeled and chopped
                directions:
                  type: string
                  default: 1) Prepare the Espresso in a small cup. 2) Fill the mixing \
glass 3/4 full with ice cubes. Add the Benedictine and the Espresso. Cool, mixing the \
ingredients with the mixing spoon. 3) Pour into the glass, filtering the ice with a strainer. \
4) Shake the cream, which should be very cold, in the mini shaker until it becomes quite thick. \
5) Rest the cream on the surface of the cocktail, making it run down the back of the mixing spoon. \
6) Garnish with a light dusting of cocoa, and serve.
        responses:
          200:
            description: Recipe updated successfully
          404:
            description: Category/recipe with id could not be found
          500:
            description: Database could not be accessed
        """
        args = self.parser.parse_args()

        messages = {}
        messages['recipe_name_message'] = validate_recipe_name(args.recipe_name.strip(), \
                category_id=category_id)
        messages['ingredients_message'] = validate_ingredients(args.ingredients)
        messages['directions_message'] = validate_directions(args.directions)

        if not data_validator(messages):
            return jsonify(messages), 400

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                recipe = Recipe.query.filter_by(id=recipe_id, category_id=category.id).first()
                if recipe:
                    recipe.recipe_name = args.recipe_name
                    recipe.ingredients = args.ingredients
                    recipe.directions = args.directions
                    recipe.save()
                    response = jsonify({
                        'id': recipe.id,
                        'recipe_name': recipe.recipe_name,
                        'ingredients': recipe.ingredients,
                        'directions': recipe.directions,
                        'category_id': recipe.category_id,
                        'date_created': recipe.date_created,
                        'date_modified': recipe.date_modified
                    })
                    response.status_code = 200
                else:
                    response = jsonify({'message': 'Sorry, recipe could not be found.'})
                    response.status_code = 404
            else:
                response = jsonify({'message': 'Sorry, recipe category could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

    def delete(self, access_token, user, category_id, recipe_id):
        """
        Process DELETE request
        ---
        tags:
          - Recipe
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of recipe category
            type: int
          - in: path
            name: recipe_id
            required: true
            description: The id of recipe requested
            type: int
        responses:
          200:
            description: Recipe updated successfully
          404:
            description: Category/recipe with id could not be found
          500:
            description: Database could not be accessed
        """

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                recipe = Recipe.query.filter_by(id=recipe_id, category_id=category.id).first()
                if recipe:
                    recipe.delete()
                    response = jsonify({'message': "Recipe {} has been deleted.". \
                            format(recipe.recipe_name)})
                    response.status_code = 200
                else:
                    response = jsonify({'message': 'Sorry, recipe could not be found.'})
                    response.status_code = 404
            else:
                response = jsonify({'message': 'Sorry, recipe category could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

class RecipeSearchView(Resource):
    """Allows for searching of a recipe."""

    method_decorators = [authenticate]

    def get(self, access_token, user, category_id):
        """
        Process GET request
        ---
        tags:
          - Recipe
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of recipe category
            type: int
          - in: query
            name: q
            description: Recipe name to search
          - in: query
            name: start
            description: id to start category results pagination
          - in: query
            name: limit
            description: Number of recipes to display per page
        responses:
          200:
            description: Recipes retrieved successfully
          400:
            description: Non-integer page and limit values submitted
          404:
            description: Category with category id could not be found
          500:
            description: Database could not be accessed
        """

        if request.values.get('q'):
            q = request.values.get('q')
        else:
            q = ''

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                recipes = Recipe.query.filter(Recipe.recipe_name.ilike('%' + q + \
                        '%')).filter_by(category_id=category_id).all()
                paginated = get_paginated_results(request, recipes, url_for('recipe_search_view', \
                        category_id=category_id) + '?q=' + q + '&')
                if paginated['is_good_query']:
                    results = []
                    for recipe in paginated['results']:
                        obj = {
                            'id': recipe.id,
                            'recipe_name': recipe.recipe_name,
                            'ingredients': recipe.ingredients,
                            'directions': recipe.directions,
                            'category_id': recipe.category_id,
                            'date_created': recipe.date_created,
                            'date_modified': recipe.date_modified
                        }
                        results.append(obj)
                    response = jsonify({
                        'results': results,
                        'previous_link': paginated['previous_link'],
                        'next_link': paginated['next_link']
                        })
                    response.status_code = 200
                else:
                    response = jsonify({'message': 'Please enter valid page and limit values.'})
                    response.status_code = 400
            else:
                response = jsonify({'message': 'Sorry, recipe category could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

recipe_view = RecipeView.as_view('recipe_view')
recipe_specific_view = RecipeSpecificView.as_view('recipe_specific_view')
recipe_search_view = RecipeSearchView.as_view('recipe_search_view')
