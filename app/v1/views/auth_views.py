""" Authentication view for user registration, login, password reset and logout """

import random
import string
from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy import exc
from app.v1.models.auth_models import User, RevokedToken
from app.v1.validators import data_validator
from app.v1.validators.auth_validators import validate_username, validate_user_email, \
        validate_password, validate_confirm_password
from app.v1.views import auth_blueprint
from app.v1.utils.decorators import authenticate
from app.v1.utils.mailer import send_mail

# pylint: disable=C0103
# pylint: disable=W0703
# pylint: disable=E1101

class RegisterView(Resource):
    """ Enables a user to create a new account. """

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='User\'s username')
    parser.add_argument('email', type=str, help='User\'s email address')
    parser.add_argument('password', type=str, help='User\'s password')
    parser.add_argument('confirm_password', type=str, help='Confirm user\'s password')

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
                username:
                  type: string
                  default: newuser
                email:
                  type: string
                  default: example@domain.com
                password:
                  type: string
                  default: Bootcamp17
                confirm_password:
                  type: string
                  default: Bootcamp17
        responses:
          201:
            description: A new user account created successfully
          400:
            description: Data validation failed
          500:
            description: Database could not be accessed
        """

        args = self.parser.parse_args()

        messages = {}
        messages['username_message'] = validate_username(args.username.strip(), register=True)
        messages['email_message'] = validate_user_email(args.email.strip(), register=True)
        messages['password_message'] = validate_password(args.password)
        messages['confirm_password_message'] = validate_confirm_password(args.confirm_password, \
                  args.password)

        if not data_validator(messages):
            return jsonify(messages), 400

        try:
            user = User(username=args.username, email=args.email, password=args.password)
            user.save()
            response = jsonify({'message': 'Your account has been created.'})
            response.status_code = 201
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

class LoginView(Resource):
    """ Enables a user to login. """

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='User\'s username')
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
                username:
                  type: string
                  default: newuser
                password:
                  type: string
                  default: Bootcamp17
        responses:
          200:
            description: User logged in to account successfully
          400:
            description: Data validation failed
          401:
            description: User authentication failed
          500:
            description: Database could not be accessed
        """

        args = self.parser.parse_args()

        messages = {}
        messages['username_message'] = validate_username(args.username.strip())
        messages['password_message'] = validate_password(args.password)

        if not data_validator(messages):
            return jsonify(messages), 400

        try:
            user = User.query.filter_by(username=args.username).first()
            if user and user.check_password(args.password):
                access_token = user.encode_token(user.id)
                if access_token:
                    response = jsonify({
                        'message': 'You are now logged in.',
                        'access_token': access_token.decode('utf-8')
                        })
                    response.status_code = 200
            else:
                response = jsonify({'message': 'Sorry, your username/password is invalid.'})
                response.status_code = 401
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

class ResetPasswordView(Resource):
    """ Enables a user to reset password. """

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='User\'s email address')

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
            description: User's email address
            type: string
            schema:
              properties:
                email:
                  type: string
                  default: ndemopaul1@gmail.com
        responses:
          200:
            description: Password reset successfully
          400:
            description: Email validation failed or email address could not be found
          500:
            description: Database could not be accessed or email could not be sent
        """

        args = self.parser.parse_args()

        messages = {}
        messages['email_message'] = validate_user_email(args.email.strip())

        if not data_validator(messages):
            return jsonify(messages), 400

        try:
            user = User.query.filter_by(email=args.email).first()
            if user:
                chars = string.ascii_uppercase + string.ascii_lowercase + \
                        string.digits
                new_password = ''.join(random.choice(chars) for i in range(8))
                user.password = user.hash_password(password=new_password)
                user.save()
                mail_content = 'Hi %s,\n\nYour password has been reset to %s. \
Please change it after login.\n\nBest regards,\nYummy Recipes Inc.' \
%(user.username, new_password)
                send_mail(user, "Yummy Recipes Password Reset", mail_content)
                response = jsonify({'message': 'Your password has been reset.'})
                response.status_code = 200
            else:
                response = jsonify({'message': 'User with this email address does not exist.'})
                response.status_code = 400
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

class ChangePasswordView(Resource):
    """ Enables a user to change password. """

    parser = reqparse.RequestParser()
    parser.add_argument('new_password', type=str, help='New user\'s password')
    parser.add_argument('confirm_new_password', type=str, help='Confirm new user\'s password')

    method_decorators = [authenticate]

    def post(self, access_token, user):
        """
        Process POST request
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            description: User's new password
            type: string
            schema:
              properties:
                new_password:
                  type: string
                  default: Bootcamp17
                confirm_new_password:
                  type: string
                  default: Bootcamp17
        responses:
          200:
            description: Password changed successfully
          400:
            description: Data validation failed
          500:
            description: Database could not be accessed or email could not be sent
        """

        args = self.parser.parse_args()

        messages = {}
        messages['new_password_message'] = validate_password(args.new_password)
        messages['confirm_new_password_message'] = validate_confirm_password(args.confirm_new_password, \
                  args.new_password)

        if not data_validator(messages):
            return jsonify(messages), 400

        try:
            user.password = user.hash_password(password=args.new_password)
            user.save()
            response = jsonify({'message': 'Your password has been changed.'})
            response.status_code = 200
        except exc.SQLAlchemyError as error:
            return jsonify({'message': str(error)}), 500
        return response

class LogoutView(Resource):
    """ Enables a user to logout. """

    method_decorators = [authenticate]

    def get(self, access_token, user):
        """
        Process GET request
        ---
        tags:
          - Auth
        security:
          - Bearer: []
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
            return jsonify({'message': str(error)}), 500
        return response

register_view = RegisterView.as_view('register_view')
login_view = LoginView.as_view('login_view')
reset_password_view = ResetPasswordView.as_view('reset_password_view')
change_password_view = ChangePasswordView.as_view('change_password_view')
logout_view = LogoutView.as_view('logout_view')

auth_blueprint.add_url_rule('/api/v1/auth/register', view_func=register_view, methods=['POST'])
auth_blueprint.add_url_rule('/api/v1/auth/login', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule('/api/v1/auth/reset_password', view_func=reset_password_view, \
        methods=['POST'])
auth_blueprint.add_url_rule('/api/v1/auth/change_password', view_func=change_password_view, \
        methods=['POST'])
auth_blueprint.add_url_rule('/api/v1/auth/logout', view_func=logout_view, methods=['GET'])
