""" Recipe view for creating, viewing, updating and deleting recipes """

from flask.views import MethodView

from flask import request, jsonify, abort, make_response
from app.auth.models import User
from app.category.models import Category
from app.recipe.models import Recipe

# pylint: disable=C0103
# pylint: disable=W0703

class RecipeView(MethodView):
    """Allows for creation and listing of recipe categories."""
    methods = ['POST', 'GET']

    def post(self):
        """Process POST request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                title = str(request.data.get('title', ''))
                ingredients = str(request.data.get('ingredients', ''))
                directions = str(request.data.get('directions', ''))
                category_id = int(request.data.get('category_id', ''))
                if title and ingredients and directions and category_id:
                    category = Category(category_name='Breakfast', user_id=user_id)
                    category.save()
                    recipe = Recipe(title=title, ingredients=ingredients, directions= \
                            directions, category_id=category_id, user_id=user_id)
                    recipe.save()
                    response = jsonify({
                        'id': recipe.id,
                        'title': recipe.title,
                        'ingredients': recipe.ingredients,
                        'directions': recipe.directions,
                        'category_id': recipe.category_id,
                        'date_created': recipe.date_created,
                        'date_modified': recipe.date_modified
                    })
                    return make_response(response), 201
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    def get(self):
        """Process GET request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipes = Recipe.query.filter_by(user_id=user_id)
                results = []
                for recipe in recipes:
                    obj = {
                        'id': recipe.id,
                        'title': recipe.title,
                        'ingredients': recipe.ingredients,
                        'directions': recipe.directions,
                        'category_id': recipe.category_id,
                        'user_id': recipe.user_id,
                        'date_created': recipe.date_created,
                        'date_modified': recipe.date_modified
                    }
                    results.append(obj)
                return make_response(jsonify(results)), 200
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

class RecipeSpecificView(MethodView):
    """Allows for viewing, updating and and deletion of specific recipe category."""
    methods = ['GET', 'PUT', 'DELETE']

    def get(self, recipe_id):
        """Process GET request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipe = Recipe.query.filter_by(id=recipe_id).first()
                if not recipe:
                    abort(404)
                response = jsonify({
                    'id': recipe.id,
                    'title': recipe.title,
                    'ingredients': recipe.ingredients,
                    'directions': recipe.directions,
                    'category_id': recipe.category_id,
                    'user_id': recipe.user_id,
                    'date_created': recipe.date_created,
                    'date_modified': recipe.date_modified
                })
                return make_response(response), 200
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    def put(self, recipe_id):
        """Process PUT request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipe = Recipe.query.filter_by(id=recipe_id).first()
                if not recipe:
                    abort(404)
                title = str(request.data.get('title', ''))
                ingredients = str(request.data.get('ingredients', ''))
                directions = str(request.data.get('directions', ''))
                category_id = int(request.data.get('category_id', ''))
                recipe.title = title
                recipe.ingredients = ingredients
                recipe.directions = directions
                recipe.category_id = category_id
                recipe.save()
                response = jsonify({
                    'id': recipe.id,
                    'title': recipe.title,
                    'ingredients': recipe.ingredients,
                    'directions': recipe.directions,
                    'category_id': recipe.category_id,
                    'user_id': recipe.user_id,
                    'date_created': recipe.date_created,
                    'date_modified': recipe.date_modified
                })
                return make_response(response), 200
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    def delete(self, recipe_id):
        """Process DELETE request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipe = Recipe.query.filter_by(id=recipe_id).first()
                if not recipe:
                    abort(404)
                recipe.delete()
                return {"message": "recipe {} has been deleted".format(recipe.id)}, 200
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

recipe_view = RecipeView.as_view('recipe_view')
recipe_specific_view = RecipeSpecificView.as_view('recipe_specific_view')
