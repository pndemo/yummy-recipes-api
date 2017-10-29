""" Category view for creating, viewing, updating and deleting categories """

from flask.views import MethodView

from flask import request, jsonify, abort, make_response
from app.auth.models import User
from app.category.models import Category

# pylint: disable=C0103
# pylint: disable=W0703

class CategoryView(MethodView):
    """Allows for creation and listing of recipe categories."""
    methods = ['GET', 'POST']

    def post(self):
        """Process POST request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category_name = str(request.data.get('category_name', ''))
                if category_name:
                    category = Category(category_name=category_name, user_id=user_id)
                    category.save()
                    response = jsonify({
                        'id': category.id,
                        'category_name': category.category_name,
                        'user_id': category.user_id,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    })
                    return make_response(response), 201
            else:
                response = {'message': user_id}
                return make_response(jsonify(response)), 401

    def get(self):
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
                categories = Category.query.filter_by(user_id=user_id).paginate(page, limit)
                results = []
                for category in categories.items:
                    obj = {
                        'id': category.id,
                        'category_name': category.category_name,
                        'user_id': category.user_id,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    }
                    results.append(obj)
                return make_response(jsonify(results)), 200
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

class CategorySpecificView(MethodView):
    """Allows for viewing, updating and and deletion of specific recipe category."""
    methods = ['GET', 'PUT', 'DELETE']

    def get(self, category_id):
        """Process GET request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Category.query.filter_by(id=category_id).first()
                if not category:
                    abort(404)
                response = jsonify({
                    'id': category.id,
                    'category_name': category.category_name,
                    'user_id': category.user_id,
                    'date_created': category.date_created,
                    'date_modified': category.date_modified
                })
                return make_response(response), 200
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    def put(self, category_id):
        """Process PUT request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Category.query.filter_by(id=category_id).first()
                if not category:
                    abort(404)
                category_name = str(request.data.get('category_name', ''))
                category.category_name = category_name
                category.save()
                response = jsonify({
                    'id': category.id,
                    'category_name': category.category_name,
                    'user_id': category.user_id,
                    'date_created': category.date_created,
                    'date_modified': category.date_modified
                })
                return make_response(response), 200
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

    def delete(self, category_id):
        """Process DELETE request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Category.query.filter_by(id=category_id).first()
                if not category:
                    abort(404)
                category.delete()
                return {"message": "category {} has been deleted". \
                        format(category.category_name)}, 200
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

class CategorySearchView(MethodView):
    """Allows for searching of a category."""
    methods = ['GET']

    def get(self):
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
                categories = Category.query.filter(Category.category_name.like('%' + q + \
                        '%')).filter_by(user_id=user_id).paginate(page, limit)
                results = []
                for category in categories.items:
                    obj = {
                        'id': category.id,
                        'category_name': category.category_name,
                        'user_id': category.user_id,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified
                    }
                    results.append(obj)
                return make_response(jsonify(results)), 200
            else:
                response = {'message': user_id}
                return make_response(jsonify(response)), 401

category_view = CategoryView.as_view('category_view')
category_specific_view = CategorySpecificView.as_view('category_specific_view')
category_search_view = CategorySearchView.as_view('category_search_view')
