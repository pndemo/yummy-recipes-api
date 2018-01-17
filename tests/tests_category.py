""" Unit tests for the category module """

import unittest
import json
from app import create_app, db

class CategoryTests(unittest.TestCase):
    """ Tests for creating, viewing, updating and deleting categories """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        register_data = {'username': 'newuser',
                         'email': 'example@domain.com',
                         'password': 'Bootcamp17',
                         'confirm_password': 'Bootcamp17'
                        }
        login_data = {'username': 'newuser', 'password': 'Bootcamp17'}
        self.category = {'category_name': 'Breakfast'}
        with self.app.app_context():
            db.create_all()
            self.client().post('/api/v1/auth/register', data=register_data)
            result = self.client().post('/api/v1/auth/login', data=login_data)
            self.access_token = json.loads(result.data.decode())['access_token']

    def test_create_valid_category(self):
        """Test API for valid creation of category (POST request)"""
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Breakfast', str(res.data))

    def test_create_empty_category_name(self):
        """Test API for unsuccessful category creation with empty category name (POST request)"""
        self.category['category_name'] = ''
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['category_name_message'], "Please enter category name.")

    def test_create_invalid_category_name(self):
        """Test API for unsuccessful category creation with invalid category name (POST request)"""
        self.category['category_name'] = 'Break#@^&'
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['category_name_message'], "Please enter a valid category name.")

    def test_create_registered_category_name(self):
        """Test API for unsuccessful category creation with registered category name (POST request)"""
        self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['category_name_message'], "A category with this category name \
is already available.")

    def test_get_categories(self):
        """Test API for retrieval of categories (GET request)"""
        self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        result = self.client().get('/api/v1/category/?start=1&limit=10', headers= \
                dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Breakfast', str(result.data))

    def test_get_category_by_id(self):
        """Test API for retrieval of specific category (GET request)"""
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        results = json.loads(res.data.decode())
        result = self.client().get('/api/v1/category/{}'.format(results['id']), \
                headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Breakfast', str(result.data))

    def test_update_category(self):
        """Test API for update of specific category (PUT request)"""
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        results = json.loads(res.data.decode())
        result = self.client().put('/api/v1/category/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + self.access_token), data={'category_name': 'Snacks'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('Snacks', str(result.data))

    def test_delete_category(self):
        """Test API for deletion of specific category (DELETE request)"""
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        results = json.loads(res.data.decode())
        res = self.client().delete('/api/v1/category/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + self.access_token))
        result = self.client().get('/api/v1/category/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(result.status_code, 404)

    def test_search_category(self):
        """Test API for category search (GET request)"""
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        results = json.loads(res.data.decode())
        res = self.client().get('/api/v1/category/search?q={}&start=1&limit=10'. \
                format(results['category_name']), headers=dict(Authorization="Bearer " + \
                self.access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))

    def tearDown(self):
        """Teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
