""" Authentication view for user registration, login, password reset and logout """

from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy import exc
from app.v1.models.auth_models import User, RevokedToken
from app.v1.validators.auth_validators import validate_user_email, validate_password
from app.v1.views import auth_blueprint
from app.v1.utils.decorators import authenticate

# pylint: disable=C0103
# pylint: disable=W0703
# pylint: disable=E1101

class RegisterView(Resource):
    """ Enables a user to create a new account. """

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='User\'s email address')
    parser.add_argument('password', type=str, help='User\'s password')

    def post(self):
        """
        Process POST request
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            description: New user's account details
            type: string
            schema:
              properties:
                email:
                  type: string
                  default: example@domain.com
                password:
                  type: string
                  default: Bootcamp17
        responses:
          201:
            description: A new user account created successfully
          400:
            description: Data validation failed
          409:
            description: A user with new user's email address is already registered
          500:
            description: Database could not be accessed
        """

        args = self.parser.parse_args()

        messages = {}
        messages['email_validation_message'] = validate_user_email(args.email)
        messages['password_validation_message'] = validate_password(args.password)

        for _, value in messages.items():
            if value != 'Valid':
                return jsonify(messages), 400

        try:
            user = User.query.filter_by(email=args.email).first()
            if not user:
                user = User(email=args.email, password=args.password)
                user.save()
                response = jsonify({'message': 'Your user account has been created.'})
                response.status_code = 201
            else:
                response = jsonify({'message': 'An account with this email address already \
exists.'})
                response.status_code = 409
        except exc.SQLAlchemyError as error:
            response = jsonify({'message': str(error)})
            response.status_code = 500
        return response

class LoginView(Resource):
    """ Enables a user to login. """

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='User\'s email address')
    parser.add_argument('password', type=str, help='User\'s password')

    def post(self):
        """
        Process POST request
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            description: Existing user's account details
            type: string
            schema:
              properties:
                email:
                  type: string
                  default: example@domain.com
                password:
                  type: string
                  default: Bootcamp17
        responses:
          200:
            description: User logged in to account successfully
          400:
            description: Data validation failed
          500:
            description: Database could not be accessed
        """

        args = self.parser.parse_args()

        messages = {}
        messages['email_validation_message'] = validate_user_email(args.email)
        messages['password_validation_message'] = validate_password(args.password)

        for _, value in messages.items():
            if value != 'Valid':
                return jsonify(messages), 400

        try:
            user = User.query.filter_by(email=args.email).first()
            if user and user.check_password(args.password):
                access_token = user.encode_token(user.id)
                if access_token:
                    response = jsonify({
                        'message': 'You are now logged in.',
                        'access_token': access_token.decode()
                        })
                    response.status_code = 200
            else:
                response = jsonify({'message': 'Sorry, your email/password is invalid.'})
                response.status_code = 401
        except exc.SQLAlchemyError as error:
            response = jsonify({'message': str(error)})
            response.status_code = 500
        return response

class ResetPasswordView(Resource):
    """ Enables a user to reset password. """

    method_decorators = [authenticate]

    parser = reqparse.RequestParser()
    parser.add_argument('current_password', type=str, help='User\'s current password')
    parser.add_argument('new_password', type=str, help='User\'s new password')
    parser.add_argument('confirm_new_password', type=str, help='Confirm user\'s new password')

    def post(self, user):
        """
        Process POST request
        ---
        tags:
          - Auth
        parameters:
          - in: header
            name: Authorization
            required: true
            type: string
          - in: body
            name: body
            required: true
            description: Current and new user's passwords
            type: string
            schema:
              properties:
                current_password:
                  type: string
                  default: Bootcamp17
                new_password:
                  type: string
                  default: Bootcamp18
                confirm_new_password:
                  type: string
                  default: Bootcamp18
        responses:
          200:
            description: Existing user logged in to account successfully
          400:
            description: Data validation failed
          401:
            description: User authentication failed
          500:
            description: Database could not be accessed
        """

        args = self.parser.parse_args()

        messages = {}
        messages['current_password_validation_message'] = validate_password(args.current_password)
        messages['new_password_validation_message'] = validate_password(args.new_password)
        messages['confirm_new_password_validation_message'] = validate_password(args.confirm_new_password)

        for _, value in messages.items():
            if value != 'Valid':
                return jsonify(messages), 400

        if user.check_password(args.current_password):
            if args.new_password == args.confirm_new_password:
                user.password = user.hash_password(password=args.new_password)
                user.save()
                response = jsonify({'message': 'Your password has been reset.'})
                response.status_code = 200
            else:
                response = jsonify({'message': 'The new passwords entered do not match.'})
                response.status_code = 400
        else:
            response = jsonify({'message': 'The current password entered is incorrect.'})
            response.status_code = 401
        return response

class LogoutView(Resource):
    """ Enables a user to logout. """

    method_decorators = [authenticate]

    def get(self, access_token, _):
        """
        Process GET request
        ---
        tags:
          - Auth
        parameters:
          - in: header
            name: Authorization
            required: true
            type: string
        responses:
          200:
            description: User logged out successfully
          401:
            description: User authentication failed
          500:
            description: Database could not be accessed
        """

        try:
            revoked_token = RevokedToken(token=access_token)
            revoked_token.save()
            response = jsonify({'message': 'Your have been logged out.'})
            response.status_code = 200
        except exc.SQLAlchemyError as error:
            response = jsonify({'message': str(error)})
            response.status_code = 500
        return response

register_view = RegisterView.as_view('register_view')
login_view = LoginView.as_view('login_view')
reset_password_view = ResetPasswordView.as_view('reset_password_view')
logout_view = LogoutView.as_view('logout_view')

auth_blueprint.add_url_rule('/api/v1/auth/register', view_func=register_view, methods=['POST'])
auth_blueprint.add_url_rule('/api/v1/auth/login', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule('/api/v1/auth/reset_password', view_func=reset_password_view, \
        methods=['POST'])
auth_blueprint.add_url_rule('/api/v1/auth/logout', view_func=logout_view, methods=['GET'])
