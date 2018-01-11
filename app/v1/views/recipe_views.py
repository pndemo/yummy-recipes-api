""" Recipe view for creating, viewing, updating and deleting recipes """

from flask.views import MethodView

from flask import request, jsonify, make_response
from app.v1.models.auth_models import User
from app.v1.models.category_models import Category
from app.v1.models.recipe_models import Recipe

# pylint: disable=C0103
# pylint: disable=W0703

class RecipeView(MethodView):
    """Allows for creation and listing of recipe categories."""
    methods = ['POST', 'GET']

    def post(self, category_id):
        """Process POST request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                try:
                    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
                    title = str(request.data.get('title', ''))
                    ingredients = str(request.data.get('ingredients', ''))
                    directions = str(request.data.get('directions', ''))
                    if title and ingredients and directions:
                        recipe = Recipe(title=title, ingredients=ingredients, directions= \
                                directions, category_id=category.id)
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
                except Exception as exp:
                    message = str(exp)
                    response = {'message': message}
                    return make_response(jsonify(response)), 404
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    def get(self, category_id):
        """Process GET request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if request.values.get('page'):
            page = int(request.values.get('page'))
        else:
            page = 1
        if request.values.get('limit'):
            limit = int(request.values.get('limit'))
        else:
            limit = 20
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                try:
                    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
                    recipes = Recipe.query.filter_by(category_id=category.id).paginate(page, limit)
                    results = []
                    for recipe in recipes.items:
                        obj = {
                            'id': recipe.id,
                            'title': recipe.title,
                            'ingredients': recipe.ingredients,
                            'directions': recipe.directions,
                            'category_id': recipe.category_id,
                            'date_created': recipe.date_created,
                            'date_modified': recipe.date_modified
                        }
                        results.append(obj)
                    return make_response(jsonify(results)), 200
                except Exception as exp:
                    message = str(exp)
                    response = {'message': message}
                    return make_response(jsonify(response)), 404
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

class RecipeSpecificView(MethodView):
    """Allows for viewing, updating and and deletion of specific recipe category."""
    methods = ['GET', 'PUT', 'DELETE']

    def get(self, category_id, recipe_id):
        """Process GET request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                try:
                    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
                    recipe = Recipe.query.filter_by(id=recipe_id, category_id=category.id).first()
                    response = jsonify({
                        'id': recipe.id,
                        'title': recipe.title,
                        'ingredients': recipe.ingredients,
                        'directions': recipe.directions,
                        'category_id': recipe.category_id,
                        'date_created': recipe.date_created,
                        'date_modified': recipe.date_modified
                    })
                    return make_response(response), 200
                except Exception as exp:
                    message = str(exp)
                    response = {'message': message}
                    return make_response(jsonify(response)), 404
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    def put(self, category_id, recipe_id):
        """Process PUT request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                try:
                    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
                    recipe = Recipe.query.filter_by(id=recipe_id, category_id=category.id).first()
                    title = str(request.data.get('title', ''))
                    ingredients = str(request.data.get('ingredients', ''))
                    directions = str(request.data.get('directions', ''))
                    recipe.title = title
                    recipe.ingredients = ingredients
                    recipe.directions = directions
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
                    return make_response(response), 200
                except Exception as exp:
                    message = str(exp)
                    response = {'message': message}
                    return make_response(jsonify(response)), 404
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    def delete(self, category_id, recipe_id):
        """Process DELETE request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                try:
                    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
                    recipe = Recipe.query.filter_by(id=recipe_id, category_id=category.id).first()
                    recipe.delete()
                    return {"message": "recipe {} has been deleted".format(recipe.title)}, 200
                except Exception as exp:
                    message = str(exp)
                    response = {'message': message}
                    return make_response(jsonify(response)), 404
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

class RecipeSearchView(MethodView):
    """Allows for searching of a recipe."""
    methods = ['GET']

    def get(self, category_id):
        """Process GET request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if request.values.get('q'):
            q = request.values.get('q')
        else:
            q = ''
        if request.values.get('page'):
            page = int(request.values.get('page'))
        else:
            page = 1
        if request.values.get('limit'):
            limit = int(request.values.get('limit'))
        else:
            limit = 20
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                try:
                    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
                    recipes = Recipe.query.filter(Recipe.title.like('%' + q + '%')). \
                            filter_by(category_id=category.id).paginate(page, limit)
                    results = []
                    for recipe in recipes.items:
                        obj = {
                            'id': recipe.id,
                            'title': recipe.title,
                            'ingredients': recipe.ingredients,
                            'directions': recipe.directions,
                            'category_id': recipe.category_id,
                            'date_created': recipe.date_created,
                            'date_modified': recipe.date_modified
                        }
                        results.append(obj)
                    return make_response(jsonify(results)), 200
                except Exception as exp:
                    message = str(exp)
                    response = {'message': message}
                    return make_response(jsonify(response)), 404
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

recipe_view = RecipeView.as_view('recipe_view')
recipe_specific_view = RecipeSpecificView.as_view('recipe_specific_view')
recipe_search_view = RecipeSearchView.as_view('recipe_search_view')
