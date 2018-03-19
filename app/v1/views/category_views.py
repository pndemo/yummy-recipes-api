""" Category view for creating, viewing, updating and deleting categories """

from flask import jsonify, request, url_for
from flask_restful import Resource, reqparse
from sqlalchemy import exc
from app.v1.models.category_models import Category
from app.v1.validators import data_validator
from app.v1.validators.category_validators import validate_category_name
from app.v1.utils.decorators import authenticate
from app.v1.utils.paginator import get_paginated_results

# pylint: disable=C0103
# pylint: disable=W0703
# pylint: disable=W0613

class CategoryView(Resource):
    """ Allows for creation and listing of recipe categories. """

    method_decorators = [authenticate]

    parser = reqparse.RequestParser()
    parser.add_argument('category_name', type=str, help='Recipes\'s category name')

    def post(self, access_token, user):
        """
        Process POST request
        ---
        tags:
          - Category
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            description: Category's category name
            type: string
            schema:
              properties:
                category_name:
                  type: string
                  default: Breakfast
        responses:
          201:
            description: A new category created successfully
          400:
            description: Data validation failed
          500:
            description: Database could not be accessed
        """

        args = self.parser.parse_args()

        messages = {}
        messages['category_name_message'] = validate_category_name(args.category_name.strip(), user.id)

        if not data_validator(messages):
            return jsonify(messages), 400

        try:
            category = Category(category_name=args.category_name, user_id=user.id)
            category.save()
            response = jsonify({
                'id': category.id,
                'category_name': category.category_name,
                'user_id': category.user_id,
                'date_created': category.date_created,
                'date_modified': category.date_modified
            })
            response.status_code = 201
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

    def get(self, access_token, user):
        """
        Process GET request
        ---
        tags:
          - Category
        security:
          - Bearer: []
        parameters:
          - in: query
            name: page
            description: Page number to display
          - in: query
            name: limit
            description: Number of categories to display per page
        responses:
          200:
            description: Categories retrieved successfully
          400:
            description: Non-integer page and limit values submitted
          500:
            description: Database could not be accessed
        """

        try:
            categories = Category.query.filter_by(user_id=user.id).all()
            paginated = get_paginated_results(request, categories, url_for('category_view') + '?')
            if paginated['is_good_query']:
                results = []
                for category in paginated['results']:
                    obj = {
                        'id': category.id,
                        'category_name': category.category_name,
                        'user_id': category.user_id,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    }
                    results.append(obj)
                response = jsonify({
                    'results': results,
                    'previous_link': paginated['previous_link'],
                    'next_link': paginated['next_link'],
                    'page': paginated['page'],
                    'pages': paginated['pages']
                    })
                response.status_code = 200
            else:
                response = jsonify({'message': 'Please enter valid page and limit values.'})
                response.status_code = 400
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

class CategorySpecificView(Resource):
    """Allows for viewing, updating and and deletion of specific recipe category."""

    method_decorators = [authenticate]

    parser = reqparse.RequestParser()
    parser.add_argument('category_name', type=str, help='Recipes\'s category name')

    def get(self, access_token, user, category_id):
        """
        Process GET request
        ---
        tags:
          - Category
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of category requested
            type: int
        responses:
          200:
            description: Category retrieved successfully
          404:
            description: Category with category id could not be found
          500:
            description: Database could not be accessed
        """

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                response = jsonify({
                    'id': category.id,
                    'category_name': category.category_name,
                    'user_id': category.user_id,
                    'date_created': category.date_created,
                    'date_modified': category.date_modified
                })
                response.status_code = 200
            else:
                response = jsonify({'message': 'Category with category id could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

    def put(self, access_token, user, category_id):
        """
        Process PUT request
        ---
        tags:
          - Category
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of category requested
            type: int
          - in: body
            name: body
            required: true
            description: Category's category name
            type: string
            schema:
              properties:
                category_name:
                  type: string
                  default: Snacks
        responses:
          200:
            description: Category updates successfully
          404:
            description: Category with category id could not be found
          500:
            description: Database could not be accessed
        """

        args = self.parser.parse_args()

        messages = {}
        messages['category_name_message'] = validate_category_name(args.category_name.strip(), user.id)

        if not data_validator(messages):
            return jsonify(messages), 400

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                category.category_name = args.category_name
                category.save()
                response = jsonify({
                    'id': category.id,
                    'category_name': category.category_name,
                    'user_id': category.user_id,
                    'date_created': category.date_created,
                    'date_modified': category.date_modified
                })
                response.status_code = 200
            else:
                response = jsonify({'message': 'Category with category id could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

    def delete(self, access_token, user, category_id):
        """
        Process DELETE request
        ---
        tags:
          - Category
        security:
          - Bearer: []
        parameters:
          - in: path
            name: category_id
            required: true
            description: The id of category requested
            type: int
        responses:
          200:
            description: Category deleted successfully
          404:
            description: Category with category id could not be found
          500:
            description: Database could not be accessed
        """

        try:
            category = Category.query.filter_by(id=category_id, user_id=user.id).first()
            if category:
                category.delete()
                response = jsonify({'message': "Category {} has been deleted". \
                        format(category.category_name)})
                response.status_code = 200
            else:
                response = jsonify({'message': 'Category with category id could not be found.'})
                response.status_code = 404
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

class CategorySearchView(Resource):
    """ Allows for searching of a category. """

    method_decorators = [authenticate]

    def get(self, access_token, user):
        """
        Process GET request
        ---
        tags:
          - Category
        security:
          - Bearer: []
        parameters:
          - in: query
            name: q
            description: Category name to search
          - in: query
            name: page
            description: Page number to display
          - in: query
            name: limit
            description: Number of categories to display per page
        responses:
          200:
            description: Categories retrieved successfully
          400:
            description: Non-integer page and limit values submitted
          500:
            description: Database could not be accessed
        """

        if request.values.get('q'):
            q = request.values.get('q')
        else:
            q = ''

        try:
            categories = Category.query.filter(Category.category_name.ilike('%' + q + \
                    '%')).filter_by(user_id=user.id).all()
            paginated = get_paginated_results(request, categories, url_for('category_search_view') + '?q=' + q + '&')
            if paginated['is_good_query']:
                results = []
                for category in paginated['results']:
                    obj = {
                        'id': category.id,
                        'category_name': category.category_name,
                        'user_id': category.user_id,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    }
                    results.append(obj)
                response = jsonify({
                    'results': results,
                    'previous_link': paginated['previous_link'],
                    'next_link': paginated['next_link'],
                    'page': paginated['page'],
                    'pages': paginated['pages']
                    })
                response.status_code = 200
            else:
                response = jsonify({'message': 'Please enter valid page and limit values.'})
                response.status_code = 400
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

category_view = CategoryView.as_view('category_view')
category_specific_view = CategorySpecificView.as_view('category_specific_view')
category_search_view = CategorySearchView.as_view('category_search_view')
