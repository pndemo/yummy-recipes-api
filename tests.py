""" Unit tests for auth, category and recipe modules """

import unittest
import json
from app import create_app, db

# pylint: disable=C0103
# pylint: disable=W0703

class AuthTests(unittest.TestCase):
    """ Authentication tests for registration, login, password_reset and logout """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {'email': 'example@domain.com', 'password': 'Bootcamp17'}
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_user_registration_unregistered(self):
        """Test API for user registration (POST request)"""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your account has been created.")

    def test_user_registration_registered(self):
        """Test API for user registration (POST request)"""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "Sorry, this user is already registered.")

    def test_user_login_registered(self):
        """Test API for user login (POST request)"""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You are now logged in.")
        self.assertTrue(result['access_token'])

    def test_user_login_non_registered(self):
        """Test API for user login (POST request)"""
        user = {'email': 'anony@domain.com', 'password': 'bootcamp'}
        res = self.client().post('/auth/login', data=user)
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Sorry, your email/password is invalid.")

    def test_password_reset(self):
        """Test API for password reset (POST request)"""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        password = {'password': 'Bootcamp172'}
        res = self.client().post('/auth/reset_password', headers=dict(Authorization="Bearer " + \
                access_token), data=password)
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your password has been reset.")

    def test_user_logout(self):
        """Test API for user logout (POST request)"""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/login', data=self.user_data)
        self.assertEqual(login_res.status_code, 200)
        result = json.loads(login_res.data.decode())
        access_token = result['access_token']
        res = self.client().post('/auth/logout', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Your have been logged out.")

class CategoryTests(unittest.TestCase):
    """ Tests for creating, viewing, updating and deleting categories """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.category = {'category_name': 'Breakfast'}
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self):
        """Helper method for registering a test user"""
        user = {'email': 'example@domain.com', 'password': 'Bootcamp17'}
        return self.client().post('/auth/register', data=user)

    def login_user(self):
        """Helper method for logging in a test user"""
        user = {'email': 'example@domain.com', 'password': 'Bootcamp17'}
        return self.client().post('/auth/login', data=user)

    def test_create_category(self):
        """Test API for POST request"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Breakfast', str(res.data))

    def test_get_all_categories(self):
        """Test API for GET request (all categories)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/category/', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))
        res = self.client().get('/category/?page=1&limit=10', headers=dict(Authorization= \
                "Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))

    def test_get_category_by_id(self):
        """Test API for GET request (specific category by id)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        result = self.client().get('/category/{}'.format(results['id']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Breakfast', str(result.data))

    def test_update_category(self):
        """Test API for PUT request"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/category/', headers=dict(Authorization="Bearer " + \
                access_token), data={'category_name': 'Desserts'})
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        res = self.client().put('/category/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token), data={'category_name': 'Snacks'})
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/category/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Snacks', str(results.data))

    def test_delete_category(self):
        """Test API for DELETE request"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/category/', headers=dict(Authorization="Bearer " + \
                access_token), data={'category_name': 'Desserts'})
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        res = self.client().delete('/category/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/category/1', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(result.status_code, 404)

    def test_search_category(self):
        """Test API for search"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/category/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.category)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/category/search?q={}'.format(self.category['category_name']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))
        res = self.client().get('/category/search?q={}&page=1&limit=10'. \
                format(self.category['category_name']), headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Breakfast', str(res.data))

class RecipeTests(unittest.TestCase):
    """ Tests for creating, viewing, updating and deleting recipes """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
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
                6) Garnish with a light dusting of cocoa, and serve.', 'category_id': 1}
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self):
        """Helper method for registering a test user"""
        user = {'email': 'example@domain.com', 'password': 'Bootcamp17'}
        return self.client().post('/auth/register', data=user)

    def login_user(self):
        """Helper method for logging in a test user"""
        user = {'email': 'example@domain.com', 'password': 'Bootcamp17'}
        return self.client().post('/auth/login', data=user)

    def test_create_recipe(self):
        """Test API for POST request"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/recipe/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Espresso Esiri', str(res.data))

    def test_get_all_recipes(self):
        """Test API for GET request (all recipes)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/recipe/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/recipe/', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Espresso Esiri', str(res.data))
        res = self.client().get('/recipe/?page=1&limit=10', headers=dict(Authorization= \
                "Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Espresso Esiri', str(res.data))


    def test_get_recipe_by_id(self):
        """Test API for GET request (specific recipe by id)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/recipe/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        result = self.client().get('/recipe/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Espresso Esiri', str(result.data))

    def test_update_recipe(self):
        """Test API for PUT request"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/recipe/', headers=dict(Authorization= \
                "Bearer " + access_token), data={'title': 'Apple Cinnamon White Cake', \
                'ingredients': '1) 1 teaspoon ground cinnamon 2) 2/3 cup white sugar \
                3) 1/2 cup butter, softened 4) 2 eggs 5) 1 1/2 teaspoons vanilla extract \
                6) 1 1/2 cups all-purpose flour 7) 1 3/4 teaspoons baking powder \
                8) 1/2 cup milk 9) 1 apple, peeled and chopped', 'directions': '1) Preheat \
                oven to 350 degrees F (175 degrees C). Grease and flour a 9x5-inch loaf pan. \
                2) Mix brown sugar and cinnamon together in a bowl. 3) Beat white sugar and \
                butter together in a bowl using an electric mixer until smooth and creamy. \
                Beat in eggs, 1 at a time, until incorporated; add vanilla extract. Lightly \
                pat apple mixture into batter. Pour the remaining batter over apple layer; \
                top with remaining apples and brown sugar mixture. 4) Bake in the preheated \
                oven until a toothpick inserted in the center of the loaf comes out clean, \
                30 to 40 minutes.', 'category_id': 1})
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        res = self.client().put('/recipe/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token), data={'title': 'Cheesy Crackers', \
                'ingredients': '1) 1/2 teaspoon vegetable oil 2) 2 tablespoons unsalted \
                butter at room temperature 3) 3/4 cup lightly packed shredded sharp Cheddar \
                cheese 4) 1/3 cup lightly packed freshly shredded Parmesan cheese \
                5) 1/2 teaspoon paprika 6) 1 pinch cayenne pepper, or to taste \
                7) 1/4 teaspoon salt 8) 1/2 cup all-purpose flour', 'directions': '1) Line \
                a baking sheet with aluminum foil and lightly grease with vegetable oil. \
                2) Place butter into a mixing bowl; add Cheddar cheese, Parmesan cheese, \
                paprika, cayenne pepper, and salt. Mix together with the back of a spatula \
                until thoroughly combined. 3) Mix flour into cheese mixture with a fork \
                until crumbly. Sprinkle in cold water, 1 or 2 drops at a time, and mix with \
                spatula until it comes together in a dough that holds its shape when \
                squeezed. 4) Transfer dough to a work surface and press into a thick, \
                flattened disk. Wrap in plastic wrap and refrigerate 30 minutes. 5) Preheat \
                oven to 375 degrees F (190 degrees C).', 'category_id': 1})
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/recipe/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Cheesy Crackers', str(results.data))

    def test_delete_recipe(self):
        """Test API for DELETE request"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/recipe/', headers=dict(Authorization= \
                "Bearer " + access_token), data={'title': 'Apple Cinnamon White Cake', \
                'ingredients': '1) 1 teaspoon ground cinnamon 2) 2/3 cup white sugar \
                3) 1/2 cup butter, softened 4) 2 eggs 5) 1 1/2 teaspoons vanilla extract \
                6) 1 1/2 cups all-purpose flour 7) 1 3/4 teaspoons baking powder \
                8) 1/2 cup milk 9) 1 apple, peeled and chopped', 'directions': '1) Preheat \
                oven to 350 degrees F (175 degrees C). Grease and flour a 9x5-inch loaf pan. \
                2) Mix brown sugar and cinnamon together in a bowl. 3) Beat white sugar and \
                butter together in a bowl using an electric mixer until smooth and creamy. \
                Beat in eggs, 1 at a time, until incorporated; add vanilla extract. Lightly \
                pat apple mixture into batter. Pour the remaining batter over apple layer; \
                top with remaining apples and brown sugar mixture. 4) Bake in the preheated \
                oven until a toothpick inserted in the center of the loaf comes out clean, \
                30 to 40 minutes.', 'category_id': 1})
        self.assertEqual(res.status_code, 201)
        results = json.loads(res.data.decode())
        res = self.client().delete('/recipe/{}'.format(results['id']), headers= \
                dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/recipe/1', headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(result.status_code, 404)

    def test_search_recipe(self):
        """Test API for search"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/recipe/', headers=dict(Authorization="Bearer " + \
                access_token), data=self.recipe)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/recipe/search?q={}'.format(self.recipe['title']), \
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Espresso Esiri', str(res.data))
        res = self.client().get('/recipe/search?q={}&page=1&limit=10'. \
                format(self.recipe['title']), headers=dict(Authorization="Bearer " + \
                access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Espresso Esiri', str(res.data))

if __name__ == "__main__":
    unittest.main()
