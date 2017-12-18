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
        self.app_invalid = create_app(config_name="testing_invalid")
        self.client_invalid = self.app_invalid.test_client
        self.user_data = {'email': 'example@domain.com', 'password': 'Bootcamp17'}
        with self.app.app_context():
            db.create_all()

    def test_user_register(self):
        """Test API for user registration (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your account has been created.")

    def test_user_registration_registered(self):
        """Test API for user registration (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "Sorry, this user is already registered.")

    def test_user_registration_invalid(self):
        """Test API for invalid user registration (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client_invalid().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 401)

    def test_user_login_registered(self):
        """Test API for user login (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You are now logged in.")
        self.assertTrue(result['access_token'])

    def test_user_login_non_registered(self):
        """Test API for unregistered user login (POST request)"""
        self.user_data['email'] = 'anony@domain.com'
        res = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Sorry, your email/password is invalid.")

    def test_password_reset(self):
        """Test API for password reset (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        password = {'password': 'Bootcamp172'}
        res = self.client().post('/api/v1/auth/reset_password', headers=dict(Authorization= \
                "Bearer " + access_token), data=password)
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your password has been reset.")

    def test_password_reset_invalid(self):
        """Test API for password reset with invalid token/database credentials (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        password = {'password': 'Bootcamp172'}
        res = self.client_invalid().post('/api/v1/auth/reset_password', headers=dict(Authorization= \
                "Bearer " + access_token), data=password)
        self.assertEqual(res.status_code, 401)
        res = self.client().post('/api/v1/auth/reset_password', headers=dict(Authorization= \
                "Bearer " + access_token + 'GyHhdE'), data=password)
        self.assertEqual(res.status_code, 401)

    def test_user_logout(self):
        """Test API for user logout (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        res = self.client().post('/api/v1/auth/logout', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your have been logged out.")

    def test_user_logout_invalid(self):
        """Test API for user logout with invalid token/database credentials (POST request)"""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        res = self.client_invalid().post('/api/v1/auth/logout', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 401)
        res = self.client().post('/api/v1/auth/logout', headers=dict(Authorization="Bearer " + \
                access_token + 'GyHhdE'))
        self.assertEqual(res.status_code, 401)

    def tearDown(self):
        """Teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
