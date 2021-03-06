""" Unit tests for the auth module """

import unittest
import json
from app import create_app, db

# pylint: disable=C0103

class AuthTests(unittest.TestCase):
    """ Authentication tests for registration, login, password_reset and logout """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.base_url = '/api/v1/auth/'
        self.register_data = {'username': 'newuser',
                              'email': 'ndemopaul@yahoo.com',
                              'password': 'Bootcamp17',
                              'confirm_password': 'Bootcamp17'
                             }
        self.login_data = {'username': 'newuser', 'password': 'Bootcamp17'}
        with self.app.app_context():
            db.create_all()

    def test_registeration_valid(self):
        """Test API for valid user registration (POST request)"""
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Your account has been created.")

    def test_registration_empty_username(self):
        """Test API for user registration with empty username (POST request)"""
        self.register_data['username'] = ''
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['username_message'], "Please enter username.")

    def test_registration_invalid_username(self):
        """Test API for user registration with invalid username (POST request)"""
        self.register_data['username'] = '@new#user'
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['username_message'], "Please enter a valid username. Username \
can only contain 5-80 alphanumeric and underscore characters.")

    def test_registration_existing_username(self):
        """Test API for user registration with existing email address (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['username_message'], "This username is already taken.")

    def test_registration_empty_email(self):
        """Test API for user registration with empty email address (POST request)"""
        self.register_data['email'] = ''
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['email_message'], "Please enter email address.")

    def test_registration_invalid_email(self):
        """Test API for user registration with invalid email (POST request)"""
        self.register_data['email'] = 'example@@domain.com'
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['email_message'], "Please enter a valid email address.")

    def test_registration_existing_email(self):
        """Test API for user registration with existing email address (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['email_message'], "This email address is already registered.")

    def test_registration_empty_password(self):
        """Test API for user registration with empty password (POST request)"""
        self.register_data['password'] = ''
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['password_message'], "Please enter password.")

    def test_registration_short_password(self):
        """Test API for user registration with short password (POST request)"""
        self.register_data['password'] = 'Boot'
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['password_message'], "Password must be at least 8 characters.")

    def test_registration_empty_confirm_password(self):
        """Test API for user registration with empty password (POST request)"""
        self.register_data['confirm_password'] = ''
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['confirm_password_message'], "Please confirm password.")

    def test_registration_non_matching_password(self):
        """Test API for user registration with short password (POST request)"""
        self.register_data['confirm_password'] = 'Bootcamp18'
        response = self.client().post(self.base_url + 'register', data=self.register_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['confirm_password_message'], "This password does not match \
the one entered.")

    def test_login_registered_valid(self):
        """Test API for registered user login with valid details (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "You are now logged in.")
        self.assertTrue(result['access_token'])

    def test_login_empty_username(self):
        """Test API for user login with empty username (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        self.login_data['username'] = ''
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['username_message'], "Please enter username.")

    def test_login_invalid_username(self):
        """Test API for user login with invalid username (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        self.login_data['username'] = '@new#user'
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['username_message'], "Please enter a valid username. Username \
can only contain 5-80 alphanumeric and underscore characters.")

    def test_login_empty_password(self):
        """Test API for user login with empty password (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        self.login_data['password'] = ''
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['password_message'], "Please enter password.")

    def test_login_short_password(self):
        """Test API for user login with short password (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        self.login_data['password'] = 'Boot'
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['password_message'], "Password must be at least 8 characters.")

    def test_login_non_registered_username(self):
        """Test API for user login with unregistered username (POST request)"""
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, your username/password is invalid.")

    def test_login_wrong_password(self):
        """Test API for user login with wrong password (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        self.login_data['password'] = 'Bootcamp18'
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, your username/password is invalid.")

    def test_password_valid_reset(self):
        """Test API for valid password reset (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        data = {'email': 'ndemopaul@yahoo.com'}
        response = self.client().post(self.base_url + 'reset_password', data=data)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertIn("Your password has been reset", result['message'])

    def test_password_reset_empty_email(self):
        """Test API for password reset with empty email address (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        data = {'email': ''}
        response = self.client().post(self.base_url + 'reset_password', data=data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['email_message'], "Please enter email address.")

    def test_password_reset_non_existent_email(self):
        """Test API for password reset with non existent email address (POST request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        data = {'email': 'ndemopaul1@yahoo.com'}
        response = self.client().post(self.base_url + 'reset_password', data=data)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "User with this email address does not exist.")

    def test_user_logout(self):
        """Test API for user logout (GET request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        response = self.client().get(self.base_url + 'logout', headers=dict(Authorization=\
                "Bearer " + access_token))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Your have been logged out.")

    def test_invalid_api_key(self):
        """Test API for API Key (GET request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        response = self.client().get(self.base_url + 'logout', headers=dict(Authorization= \
                "Bearer " + access_token + 'DhGdy'))
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, user could not be found.")

    def test_incorrect_format_api_key(self):
        """Test API for Key submitted in incorrect format (GET request)"""
        self.client().post(self.base_url + 'register', data=self.register_data)
        response = self.client().post(self.base_url + 'login', data=self.login_data)
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        response = self.client().get(self.base_url + 'logout', headers=dict(Authorization= \
                "Bearer" + access_token))
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, user could not be authenticated.")

    def tearDown(self):
        """Teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
