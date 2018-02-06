""" Unit tests for the category module """

import unittest
import json
from app import create_app, db

# pylint: disable=C0103

class CategoryTests(unittest.TestCase):
    """ Tests for creating, viewing, updating and deleting categories """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.base_url = '/api/v1/category/'
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
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Breakfast', str(response.data))

    def test_create_empty_category_name(self):
        """Test API for unsuccessful category creation with empty category name (POST request)"""
        self.category['category_name'] = ''
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['category_name_message'], "Please enter category name.")

    def test_create_invalid_category_name(self):
        """Test API for unsuccessful category creation with invalid category name (POST request)"""
        self.category['category_name'] = 'Break#@^&'
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['category_name_message'], "Please enter a valid category name.")

    def test_create_registered_category_name(self):
        """Test API for category creation with registered category name (POST request)"""
        self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['category_name_message'], "A category with this category name \
is already available.")

    def test_get_categories_set_values(self):
        """Test API for retrieval of categories with set page and limit values (GET request)"""
        self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        response = self.client().get(self.base_url + '?page=1&limit=10', headers= \
                dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Breakfast', str(response.data))

    def test_get_categories_default_values(self):
        """Test API for retrieval of categories with default page and limit values (GET request)"""
        self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        response = self.client().get(self.base_url, headers=dict(Authorization= \
                "Bearer " + self.access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Breakfast', str(response.data))

    def test_get_categories_invalid_values(self):
        """Test API for retrieval of categories with invalid page and limit values (GET request)"""
        self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        response = self.client().get(self.base_url + '?page=ws&limit=10', headers= \
                dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Please enter valid page and limit values.")

    def test_get_category_by_valid_id(self):
        """Test API for retrieval of specific category with valid category id (GET request)"""
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        result = json.loads(response.data.decode())
        response = self.client().get(self.base_url + '{}'.format(result['id']), \
                headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Breakfast', str(response.data))

    def test_get_category_by_invalid_id(self):
        """Test API for retrieval of specific category with invalid category id (GET request)"""
        response = self.client().get(self.base_url + '1', headers=dict(Authorization= \
                "Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Category with category id could not be found.")

    def test_update_valid_category_name(self):
        """Test API for update of specific category with valid category name (PUT request)"""
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        result = json.loads(response.data.decode())
        self.category['category_name'] = 'Snacks'
        response = self.client().put(self.base_url + '{}'.format(result['id']), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.category)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Snacks', str(response.data))

    def test_update_registered_category_name(self):
        """Test API for update of specific category with registered category name (PUT request)"""
        self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        self.category['category_name'] = 'Snacks'
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        result = json.loads(response.data.decode())
        self.category['category_name'] = 'Breakfast'
        response = self.client().put(self.base_url + '{}'.format(result['id']), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.category)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['category_name_message'], "A category with this category name \
is already available.")

    def test_update_category_by_invalid_id(self):
        """Test API for update of specific category with invalid category id (GET request)"""
        response = self.client().put(self.base_url + '1', headers=dict(Authorization= \
                "Bearer " + self.access_token), data=self.category)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Category with category id could not be found.")

    def test_delete_category_valid_id(self):
        """Test API for deletion of specific category with valid id (DELETE request)"""
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        result = json.loads(response.data.decode())
        self.client().delete(self.base_url + '{}'.format(result['id']), headers= \
                dict(Authorization="Bearer " + self.access_token))
        response = self.client().get(self.base_url + '{}'.format(result['id']), headers= \
                dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)

    def test_delete_category_by_invalid_id(self):
        """Test API for delete of specific category with invalid id (GET request)"""
        response = self.client().delete(self.base_url + '1', headers=dict(Authorization= \
                "Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Category with category id could not be found.")

    def test_search_category_valid_page_limit(self):
        """Test API for category search with valid page and limit values (GET request)"""
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        result = json.loads(response.data.decode())
        response = self.client().get(self.base_url + 'search?q={}&page=1&limit=10'. \
                format(result['category_name']), headers=dict(Authorization="Bearer " + \
                self.access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Breakfast', str(response.data))

    def test_search_category_invalid_page_limit(self):
        """Test API for category search with invalid page and limit values (GET request)"""
        response = self.client().post(self.base_url, headers=dict(Authorization="Bearer " + \
                self.access_token), data=self.category)
        result = json.loads(response.data.decode())
        response = self.client().get(self.base_url + 'search?q={}&page=1q&limit=jx'. \
                format(result['category_name']), headers=dict(Authorization="Bearer " + \
                self.access_token))
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Please enter valid page and limit values.")

    def tearDown(self):
        """Teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
