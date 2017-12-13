<h1>Yummy Recipes API</h1>
<a href="https://www.codacy.com/app/pndemo/yummy-recipes?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pndemo/yummy-recipes&amp;utm_campaign=Badge_Grade">
<img class="notice-badge" src="https://api.codacy.com/project/badge/Grade/1512eaed87c44b8794ca3aae2154c76b" alt="Badge"/>
</a>
<a href="https://travis-ci.org/pndemo/yummy-recipes-api">
<img class="notice-badge" src="https://travis-ci.org/pndemo/yummy-recipes-api.svg?branch=develop" alt="Badge"/>
</a>
<a href="https://coveralls.io/github/pndemo/yummy-recipes-api">
<img class="notice-badge" src="https://coveralls.io/repos/github/pndemo/yummy-recipes-api/badge.svg?branch=develop" alt="Badge"/>
</a>
<a href="https://www.python.org/dev/peps/pep-0008/">
<img class="notice-badge" src="https://img.shields.io/badge/code%20style-pep8-orange.svg" alt="Badge"/>
</a>
<a href="https://github.com/pndemo/yummy-recipes-api/blob/develop/Licence.md">
<img class="notice-badge" src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="Badge"/>
</a>
<br/>
<h2>About Yummy Recipes API</h2>
This app enables you to access Yummy Recipes resources, a platform for users to keep track of their awesome recipes and share with others if they so wish. The API functionalities include: creation of new user accounts, user login, password reset, creation of new recipe categories, viewing of recipe categories, updating of recipe categories, deletion of recipe categories, creation of new recipes, viewing of recipes, updating of recipes and deletion of recipes.
<br/>
<h2>Installation</h2>
<ol>
  <li>Install Python (preferably, version >= 3.5).</li>
  <li>Clone Yummy Recipes API from GitHub to your local machine.</li>
  <p><code>$ git clone https://github.com/pndemo/yummy-recipes-api.git</code></p>
  <li>Change directory to yummy-recipes-api</li>
  <p><code>$ cd yummy-recipes-api</code></p>
  <li>Create virtual environment</li>
  <p><code>$ virtualenv venv</code></p>
  <li>Activate virtual environment</li>
  <p><code>$ source venv/bin/activate</code></p>
  <li>Install application requirements in virtual environment</li>
  <p><code>$ pip install -r requirements.txt</code></p>
  <li>Run the application</li>
  <p><code>$ export FLASK_APP=run.py</code></p>
  <p><code>$ flask run</code></p>
</ol>
<h2>API Endpoints</h2>
1) Auth module

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
GET/POST /api/v1/auth/register | Create a new user account | PUBLIC
GET/POST /api/v1/auth/login | Login registered user | PUBLIC
GET/POST /api/v1/auth/reset_password | Change user's password | PRIVATE
GET/POST /api/v1/auth/logout | Logout logged in user | PRIVATE

2) Category module

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
GET /api/v1/category/ | Get user's categories | PRIVATE
POST /api/v1/category/ | Create a new category | PRIVATE
GET /api/v1/category/<int:category_id> | Get a specific category given category_id | PRIVATE
PUT /api/v1/category/<int:category_id> | Update a specific category given category_id | PRIVATE
DELETE /api/v1/category/<int:category_id> | Delete a specific category given category_id | PRIVATE
GET /api/v1/category/search | Search for category using category name | PRIVATE

3) Recipe module

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
GET /api/v1/recipe/<int:category_id>/ | Get user's recipes given category_id | PRIVATE
POST /api/v1/recipe/<int:category_id>/ | Create a new category given category_id | PRIVATE
GET /api/v1/recipe/<int:category_id>/<int:recipe_id> | Get a specific recipe given category_id and recipe_id | PRIVATE
PUT /api/v1/recipe/<int:category_id>/<int:recipe_id> | Update a specific recipe given category_id and recipe_id | PRIVATE
DELETE /api/v1/recipe/<int:category_id>/<int:recipe_id> | Delete a specific recipe given category_id and recipe_id | PRIVATE
GET /api/v1/recipe/<int:category_id>/search | Search for recipe given category_id using recipe name | PRIVATE

<h2>Demo API</h2>
<p>The demo API of the Yummy Recipes API app can be accessed using the link below.</p>
<p><a href="https://sandbx.herokuapp.com/">https://sandbx.herokuapp.com/</p>
<h2>Testing</h2>
<p>Testing has been implemented using the unit testing framework of the Python language. To run tests, use the following command:</p>
<p><code>$ nosetests</code></p>
<h2>Licensing</h2>
<p>This app is licensed under the MIT license.</p>
