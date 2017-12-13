""" Unit tests for the recipe module """

import unittest
import json
from app import create_app, db

class RecipeTests(unittest.TestCase):
    """ Tests for creating, viewing, updating and deleting recipes """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {'email': 'example@domain.com', 'password': 'Bootcamp17'}
        self.category = {'category_name': 'Breakfast'}
        self.recipe = {'title': 'Espresso Esiri', 'ingredients': '1) 1 tbsp plus 1 or 2 tsp \
                (20-25 ml) Espresso, 2) 2 tbsp (30 ml) Benedictine, 3) Approx. 3 tbsp \
                (40 ml) fresh heavy cream, 4) Unsweetened cocoa powder, 5) Ice cubes', \
                'directions': '1) Prepare the Espresso in a small cup. 2) Fill the mixing \
                glass 3/4 full with ice cubes. Add the Benedictine and the Espresso. Cool, \
                mixing the ingredients with the mixing spoon. 3) Pour into the glass, \
                filtering the ice with a strainer. 4) Shake the cream, which should be very \
                cold, in the mini shaker until it becomes quite thick. 5) Rest the cream on \
                the surface of the cocktail, making it run down the back of the mixing spoon. \
                6) Garnish with a light dusting of cocoa, and serve.'}
        with self.app.app_context():
            db.create_all()

    def test_create_recipe(self):
        """Test API for POST request"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        category_id = results['id']
        res = self.client().post('/api/v1/recipe/{}/'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Espresso Esiri', str(res.data))

    def test_get_all_recipes(self):
        """Test API for GET request (all recipes)"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        category_id = results['id']
        res = self.client().post('/api/v1/recipe/{}/'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/recipe/{}/'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Espresso Esiri', str(res.data))
        res = self.client().get('/api/v1/recipe/{}/?page=1&limit=10'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Espresso Esiri', str(res.data))


    def test_get_recipe_by_id(self):
        """Test API for GET request (specific recipe by id)"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        category_id = results['id']
        res = self.client().post('/api/v1/recipe/{}/'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        result = self.client().get('/api/v1/recipe/{}/{}'.format(category_id, results['id']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Espresso Esiri', str(result.data))

    def test_update_recipe(self):
        """Test API for PUT request"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        category_id = results['id']
        res = self.client().post('/api/v1/recipe/1/'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        self.recipe['title'] = 'Apple Cinnamon White Cake'
        self.recipe['ingredients'] = '1) 1 teaspoon ground cinnamon 2) 2/3 cup white sugar \
                3) 1/2 cup butter, softened 4) 2 eggs 5) 1 1/2 teaspoons vanilla extract \
                6) 1 1/2 cups all-purpose flour 7) 1 3/4 teaspoons baking powder \
                8) 1/2 cup milk 9) 1 apple, peeled and chopped'
        self.recipe['directions'] = '1) Preheat oven to 350 degrees F (175 degrees C). \
                Grease and flour a 9x5-inch loaf pan. 2) Mix brown sugar and cinnamon together \
                in a bowl. 3) Beat white sugar and butter together in a bowl using an electric \
                mixer until smooth and creamy. Beat in eggs, 1 at a time, until incorporated; \
                add vanilla extract. Lightly pat apple mixture into batter. Pour the remaining \
                batter over apple layer; top with remaining apples and brown sugar mixture. \
                4) Bake in the preheated oven until a toothpick inserted in the center of the \
                loaf comes out clean, 30 to 40 minutes.'
        res = self.client().put('/api/v1/recipe/{}/{}'.format(category_id, results['id']), \
                headers=dict(Authorization="Bearer " + access_token), data=self.recipe)
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/api/v1/recipe/{}/{}'.format(category_id, results['id']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Apple Cinnamon White Cake', str(results.data))

    def test_delete_recipe(self):
        """Test API for DELETE request"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        category_id = results['id']
        res = self.client().post('/api/v1/recipe/{}/'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        res = self.client().delete('/api/v1/recipe/{}/{}'.format(category_id, results['id']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/api/v1/recipe/{}/{}'.format(category_id, results['id']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_search_recipe(self):
        """Test API for search"""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        result = self.client().post('/api/v1/auth/login', data=self.user_data)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/api/v1/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        category_id = results['id']
        res = self.client().post('/api/v1/recipe/{}/'.format(category_id), headers= \
                dict(Authorization="Bearer " + access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/recipe/{}/search?q={}'.format(category_id, \
                self.recipe['title']), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Espresso Esiri', str(res.data))
        res = self.client().get('/api/v1/recipe/{}/search?q={}&page=1&limit=10'. \
                format(category_id, self.recipe['title']), headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Espresso Esiri', str(res.data))

    def tearDown(self):
        """Teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
