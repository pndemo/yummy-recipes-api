""" Authentication view for registration, login, password_reset and logot """

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.auth.models import User, RevokedToken
from app.auth import auth_blueprint

# pylint: disable=C0103
# pylint: disable=W0703

class RegisterView(MethodView):
    """Allows user to create a new account."""

    def post(self):
        """Process POST request"""
        user = User.query.filter_by(email=request.data['email']).first()
        if not user:
            try:
                post_data = request.data
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                user.save()
                response = {'message': 'Your account has been created.'}
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 401
        else:
            response = {'message': 'Sorry, this user is already registered.'}
            return make_response(jsonify(response)), 202

class LoginView(MethodView):
    """Allows user login to account."""

    def post(self):
        """Process POST request"""
        try:
            user = User.query.filter_by(email=request.data['email']).first()
            if user and user.check_password(request.data['password']):
                access_token = user.encode_token(user.id)
                if access_token:
                    response = {
                        'message': 'You are now logged in.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {'message': 'Sorry, your email/password is invalid.'}
                return make_response(jsonify(response)), 401
        except Exception as exp:
            response = {'message': str(exp)}
            return make_response(jsonify(response)), 500

class ResetPasswordView(MethodView):
    """Allows user to reset password."""

    def post(self):
        """Process POST request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                try:
                    user = User.query.filter_by(id=user_id).first()
                    password = request.data['password']
                    user.password = user.hash_password(password=password)
                    user.save()
                    response = {'message': 'Your password has been reset.'}
                    return make_response(jsonify(response)), 200
                except Exception as exp:
                    response = {'message': str(exp)}
                    return make_response(jsonify(response)), 401
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

class LogoutView(MethodView):
    """Allows user to logout from account."""

    def post(self):
        """Process POST request"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                try:
                    revoked_token = RevokedToken(token=access_token)
                    revoked_token.save()
                    response = {'message': 'Your have been logged out.'}
                    return make_response(jsonify(response)), 200
                except Exception as exp:
                    response = {'message': str(exp)}
                    return make_response(jsonify(response)), 401
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response)), 401

register_view = RegisterView.as_view('register_view')
login_view = LoginView.as_view('login_view')
reset_password_view = ResetPasswordView.as_view('reset_password_view')
logout_view = LogoutView.as_view('logout_view')
auth_blueprint.add_url_rule('/auth/register', view_func=register_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/reset_password', view_func=reset_password_view, \
        methods=['POST'])
auth_blueprint.add_url_rule('/auth/logout', view_func=logout_view, methods=['POST'])
