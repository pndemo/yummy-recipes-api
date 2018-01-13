""" Unit tests for the auth module """

import unittest
import json
from app import create_app, db

class AuthTests(unittest.TestCase):
    """ Authentication tests for registration, login, password_reset and logout """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.register_data = {'username': 'newuser',
                              'email': 'example@domain.com',
                              'password': 'Bootcamp17',
                              'confirm_password': 'Bootcamp17'
                             }
        self.login_data = {'username': 'newuser',
                           'password': 'Bootcamp17'
                          }
        with self.app.app_context():
            db.create_all()

    def test_user_registeration_valid(self):
        """Test API for valid user registration (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your account has been created.")

    def test_user_registration_empty_fields(self):
        """Test API for user registration with empty fields (POST request)"""
        self.register_data['username'] = ''
        self.register_data['email'] = ''
        self.register_data['password'] = ''
        self.register_data['confirm_password'] = ''
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['username_message'], "Please enter username.")
        self.assertEqual(result['email_message'], "Please enter email address.")
        self.assertEqual(result['password_message'], "Please enter password.")
        self.assertEqual(result['confirm_password_message'], "Please enter password.")

    def test_user_registration_invalid_username(self):
        """Test API for user registration with invalid username (POST request)"""
        self.register_data['username'] = '@new#user'
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['username_message'], "Please enter a valid username. Username \
can only contain 5-80 alphanumeric and underscore characters.")

    def test_user_registration_invalid_email(self):
        """Test API for user registration with invalid email (POST request)"""
        self.register_data['email'] = 'example@@domain.com'
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['email_message'], "Please enter a valid email address.")

    def test_user_registration_short_password(self):
        """Test API for user registration with short password (POST request)"""
        self.register_data['password'] = 'Boot'
        self.register_data['confirm_password'] = 'Boot'
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['password_message'], "Password must be at least 8 characters.")
        self.assertEqual(result['confirm_password_message'], "Password must be at least 8 characters.")

    def test_user_registration_existing_username(self):
        """Test API for user registration with existing email address (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['username_message'], "This username is already taken.")

    def test_user_registration_existing_email(self):
        """Test API for user registration with existing email address (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['email_message'], "This email address is already registered.")

    def test_user_registration_non_matching_password(self):
        """Test API for user registration with short password (POST request)"""
        self.register_data['confirm_password'] = 'Bootcamp18'
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['confirm_password_message'], "This password does not match \
the one entered.")

    def test_user_login_registered(self):
        """Test API for registered user login (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You are now logged in.")
        self.assertTrue(result['access_token'])

    def test_user_login_empty_fields(self):
        """Test API for user login with empty fields (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        self.login_data['username'] = ''
        self.login_data['password'] = ''
        res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['username_message'], "Please enter username.")
        self.assertEqual(result['password_message'], "Please enter password.")

    def test_user_login_non_registered(self):
        """Test API for unregistered user login (POST request)"""
        res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Sorry, your email/password is invalid.")

    def test_password_reset(self):
        """Test API for password reset (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        data = {'current_password': 'Bootcamp17',
                'new_password': 'Bootcamp18',
                'confirm_new_password': 'Bootcamp18'
               }
        res = self.client().post('/api/v1/auth/reset_password', headers=dict(Authorization= \
                "Bearer " + access_token), data=data)
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your password has been reset.")

    def test_password_reset_empty_fields(self):
        """Test API for password reset with empty fields (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        data = {'current_password': '',
                'new_password': '',
                'confirm_new_password': ''
               }
        res = self.client().post('/api/v1/auth/reset_password', headers=dict(Authorization= \
                "Bearer " + access_token), data=data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['current_password_message'], "Please enter password.")
        self.assertEqual(result['new_password_message'], "Please enter password.")
        self.assertEqual(result['confirm_new_password_message'], "Please enter password.")

    def test_password_reset_wrong_current_password(self):
        """Test API for password reset with wrong current password (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        data = {'current_password': 'Bootcamp18',
                'new_password': 'Bootcamp18',
                'confirm_new_password': 'Bootcamp18'
               }
        res = self.client().post('/api/v1/auth/reset_password', headers=dict(Authorization= \
                "Bearer " + access_token), data=data)
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "The current password entered is incorrect.")

    def test_password_reset_short_password(self):
        """Test API for password reset with short password (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        data = {'current_password': 'Bootcamp17',
                'new_password': 'Boot',
                'confirm_new_password': 'Boot'
               }
        res = self.client().post('/api/v1/auth/reset_password', headers=dict(Authorization= \
                "Bearer " + access_token), data=data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['new_password_message'], "Password must be at least 8 characters.")
        self.assertEqual(result['confirm_new_password_message'], "Password must be at least 8 characters.")

    def test_password_reset_non_matching_passwords(self):
        """Test API for password reset with non matching passwords (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        data = {'current_password': 'Bootcamp17',
                'new_password': 'Bootcamp18',
                'confirm_new_password': 'Bootcamp19'
               }
        res = self.client().post('/api/v1/auth/reset_password', headers=dict(Authorization= \
                "Bearer " + access_token), data=data)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['confirm_new_password_message'], "This password does not match \
the one entered.")

    def test_user_logout(self):
        """Test API for user logout (GET request)"""
        res = self.client().post('/api/v1/auth/register', data=self.register_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.login_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        res = self.client().get('/api/v1/auth/logout', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your have been logged out.")

    def tearDown(self):
        """Teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
