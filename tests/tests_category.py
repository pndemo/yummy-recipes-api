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
        self.user_data = {'email': 'example@domain.com', 'password': 'Bootcamp17'}
        self.category = {'category_name': 'Breakfast'}
        with self.app.app_context():
            db.create_all()

    def test_create_category(self):
        """Test API for POST request"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Breakfast', str(res.data))

    def test_get_all_categories(self):
        """Test API for GET request (all categories)"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))
        res = self.client().get('/api/v1/category/?page=1&limit=10', headers=dict(Authorization= \
                "Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))

    def test_get_category_by_id(self):
        """Test API for GET request (specific category by id)"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        result = self.client().get('/api/v1/category/{}'.format(results['id']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Breakfast', str(result.data))

    def test_update_category(self):
        """Test API for PUT request"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data={'category_name': 'Desserts'})
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        res = self.client().put('/api/v1/category/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token), data={'category_name': 'Snacks'})
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/api/v1/category/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Snacks', str(results.data))

    def test_delete_category(self):
        """Test API for DELETE request"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data={'category_name': 'Desserts'})
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        category_id = results['id']
        res = self.client().delete('/api/v1/category/{}'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/api/v1/category/{}'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_search_category(self):
        """Test API for search"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/category/search?q={}'.format(self.category['category_name']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))
        res = self.client().get('/api/v1/category/search?q={}&page=1&limit=10'. \
                format(self.category['category_name']), headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))

    def tearDown(self):
        """Teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
