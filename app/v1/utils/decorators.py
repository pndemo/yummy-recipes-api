""" Decorator functions for auth, category and recipe modules """

from functools import wraps
from flask import request, jsonify
from sqlalchemy import exc
from app.v1.models.auth_models import User

def authenticate(func):
    """ Authenticates user using accesss token in authorization header. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ Authentication wrapper. """
        try:
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(' ')[1]
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                user = User.query.filter_by(id=user_id).first()
                return func(access_token, user, *args, **kwargs)
            else:
                response = jsonify({'message': 'Sorry, user could not be found.'})
                response.status_code = 401
        except IndexError:
            response = jsonify({'message': 'Sorry, user could not be authenticated.'})
            response.status_code = 401
        except exc.SQLAlchemyError as error:
            response = jsonify({'message': str(error)})
            response.status_code = 500
        return response
    return wrapper
