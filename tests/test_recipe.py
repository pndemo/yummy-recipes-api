""" Unit tests for the recipe module """

import unittest
import json
from app import create_app, db

# pylint: disable=C0103

class RecipeTests(unittest.TestCase):
    """ Tests for creating, viewing, updating and deleting recipes """

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.base_url = '/api/v1/recipe/'
        register_data = {'username': 'newuser',
                         'email': 'example@domain.com',
                         'password': 'Bootcamp17',
                         'confirm_password': 'Bootcamp17'
                        }
        login_data = {'username': 'newuser', 'password': 'Bootcamp17'}
        category = {'category_name': 'Breakfast'}
        self.recipe = {'recipe_name': 'Espresso Esiri',
                       'ingredients': '1) 1 tbsp plus 1 or 2 tsp \
(20-25 ml) Espresso, 2) 2 tbsp (30 ml) Benedictine, 3) Approx. 3 tbsp (40 ml) fresh heavy cream, \
4) Unsweetened cocoa powder, 5) Ice cubes',
                       'directions': '1) Prepare the Espresso in a small cup. \
2) Fill the mixing glass 3/4 full with ice cubes. Add the Benedictine and the Espresso. Cool, \
mixing the ingredients with the mixing spoon. 3) Pour into the glass, filtering the ice with a \
strainer. 4) Shake the cream, which should be very cold, in the mini shaker until it becomes \
quite thick. 5) Rest the cream on the surface of the cocktail, making it run down the back of \
the mixing spoon. 6) Garnish with a light dusting of cocoa, and serve.'
                      }
        with self.app.app_context():
            db.create_all()
            self.client().post('/api/v1/auth/register', data=register_data)
            result = self.client().post('/api/v1/auth/login', data=login_data)
            self.access_token = json.loads(result.data.decode())['access_token']
            result = self.client().post('/api/v1/category/', headers=dict(Authorization=\
                        "Bearer " + self.access_token), data=category)
            self.category_id = json.loads(result.data.decode())['id']

    def test_create_valid_recipe(self):
        """Test API for valid creation of recipe (POST request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Espresso Esiri', str(response.data))

    def test_create_recipe_invalid_category(self):
        """Test API for creation of recipe with invalid category id (POST request)"""
        response = self.client().post(self.base_url + '2/', headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe category could not be found.")

    def test_create_empty_recipe_name(self):
        """Test API for unsuccessful recipe creation with empty recipe name (POST request)"""
        self.recipe['recipe_name'] = ''
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['recipe_name_message'], "Please enter recipe name.")

    def test_create_invalid_recipe_name(self):
        """Test for unsuccessful recipe creation with invalid recipe name (POST request)"""
        self.recipe['recipe_name'] = 'Espresso E#%@h'
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['recipe_name_message'], "Please enter a valid recipe name.")

    def test_create_registered_recipe_name(self):
        """Test for unsuccessful recipe creation with registered recipe name (POST request)"""
        self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['recipe_name_message'], "A recipe with this recipe name \
is already available.")

    def test_create_empty_ingredients(self):
        """Test API for unsuccessful recipe creation with empty ingredients (POST request)"""
        self.recipe['ingredients'] = ''
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['ingredients_message'], "Please enter ingredients.")

    def test_create_empty_directions(self):
        """Test API for unsuccessful recipe creation with empty directions (POST request)"""
        self.recipe['directions'] = ''
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['directions_message'], "Please enter directions.")

    def test_get_recipes_valid_category(self):
        """Test API for retrieval of recipes with valid category  (GET request)"""
        self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        response = self.client().get(self.base_url + '{}/?page=1&limit=10'. \
                format(self.category_id), headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Espresso Esiri', str(response.data))

    def test_get_recipes_invalid_category(self):
        """Test API for retrieval of recipes with invalid category id (GET request)"""
        response = self.client().get(self.base_url + '2/', headers=dict(Authorization= \
                "Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe category could not be found.")

    def test_get_recipes_invalid_page_limit(self):
        """Test API for retrieval of recipes with invalid page/limit values (GET request)"""
        self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        response = self.client().get(self.base_url + '{}/?page=qw&limit=gh'. \
                format(self.category_id), headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Please enter valid page and limit values.")

    def test_get_recipe_by_id_valid(self):
        """Test API for retrieval of specific valid recipe id (GET request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        result = json.loads(response.data.decode())
        response = self.client().get(self.base_url + '{}/{}'.format(self.category_id, \
                result['id']), headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Espresso Esiri', str(response.data))

    def test_get_recipe_invalid_category(self):
        """Test API for retrieval of specific recipe with invalid category id (GET request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        result = json.loads(response.data.decode())
        response = self.client().get(self.base_url + '2/{}'.format(result['id']), \
                headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe category could not be found.")

    def test_get_recipe_by_id_invalid(self):
        """Test API for retrieval of specific invalid recipe id (GET request)"""
        response = self.client().get(self.base_url + '{}/2'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe could not be found.")

    def test_update_recipe_valid_data(self):
        """Test API for update of specific recipe with valid data (PUT request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        result = json.loads(response.data.decode())
        self.recipe['recipe_name'] = 'Apple Cinnamon White Cake'
        self.recipe['ingredients'] = '1) 1 teaspoon ground cinnamon 2) 2/3 cup white sugar \
3) 1/2 cup butter, softened 4) 2 eggs 5) 1 1/2 teaspoons vanilla extract 6) 1 1/2 cups all-purpose \
flour 7) 1 3/4 teaspoons baking powder 8) 1/2 cup milk 9) 1 apple, peeled and chopped'
        response = self.client().put(self.base_url + '{}/{}'.format(self.category_id, \
                result['id']), headers=dict(Authorization="Bearer " + self.access_token), \
                data=self.recipe)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Apple Cinnamon White Cake', str(response.data))

    def test_update_recipe_invalid_id(self):
        """Test API for update of specific recipe with invalid id (PUT request)"""
        self.recipe['recipe_name'] = 'Apple Cinnamon White Cake'
        response = self.client().put(self.base_url + '{}/2'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe could not be found.")

    def test_update_recipe_invalid_category_id(self):
        """Test API for update of specific recipe with invalid category id (PUT request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.recipe['recipe_name'] = 'Apple Cinnamon White Cake'
        result = json.loads(response.data.decode())
        response = self.client().put(self.base_url + '2/{}'.format(result['id']), \
                headers=dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe category could not be found.")

    def test_update_recipe_registered_recipe_name(self):
        """Test API for update of specific recipe (PUT request)"""
        self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.recipe['recipe_name'] = 'Apple Cinnamon White Cake'
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        self.recipe['recipe_name'] = 'Espresso Esiri'
        result = json.loads(response.data.decode())
        response = self.client().put(self.base_url + '{}/{}'.format(self.category_id, \
                result['id']), headers=dict(Authorization="Bearer " + self.access_token), \
                data=self.recipe)
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['recipe_name_message'], "A recipe with this recipe name \
is already available.")

    def test_delete_recipe_valid_id(self):
        """Test API for deletion of specific recipe with valid id (DELETE request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        result = json.loads(response.data.decode())
        self.client().delete(self.base_url + '{}/{}'.format(self.category_id, \
                result['id']), headers=dict(Authorization="Bearer " + self.access_token))
        response = self.client().get(self.base_url + '{}/{}'.format(self.category_id, \
                result['id']), headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)

    def test_delete_recipe_invalid_id(self):
        """Test API for deletion of specific recipe with invalid id (DELETE request)"""
        response = self.client().delete(self.base_url + '{}/2'.format(self.category_id), \
                headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe could not be found.")

    def test_delete_recipe_invalid_category_id(self):
        """Test API for deletion of specific recipe with invalid category id (DELETE request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        result = json.loads(response.data.decode())
        response = self.client().delete(self.base_url + '2/{}'.format(result['id']), \
                headers=dict(Authorization="Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe category could not be found.")

    def test_search_recipe_valid_page_limit(self):
        """Test API for recipe search with valid page/limit values (GET request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        result = json.loads(response.data.decode())
        response = self.client().get(self.base_url + '{}/search?q={}&page=1&limit=10'. \
                format(self.category_id, result['recipe_name']), headers=dict(Authorization= \
                "Bearer " + self.access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Espresso Esiri', str(response.data))

    def test_search_recipe_invalid_page_limit(self):
        """Test API for recipe search with invalid page/limit values (GET request)"""
        response = self.client().post(self.base_url + '{}/'.format(self.category_id), headers= \
                dict(Authorization="Bearer " + self.access_token), data=self.recipe)
        result = json.loads(response.data.decode())
        response = self.client().get(self.base_url + '{}/search?q={}&page=1t&limit=5y'. \
                format(self.category_id, result['recipe_name']), headers=dict(Authorization= \
                "Bearer " + self.access_token))
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Please enter valid page and limit values.")

    def test_search_recipe_invalid_category(self):
        """Test API for recipe search with invalid category id (GET request)"""
        response = self.client().get(self.base_url + '2/search?q={}&page=1t&limit=5y'. \
                format(self.recipe['recipe_name']), headers=dict(Authorization= \
                "Bearer " + self.access_token))
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Sorry, recipe category could not be found.")

    def tearDown(self):
        """Teardown initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
