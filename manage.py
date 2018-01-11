""" Manage migrations """

# pylint: disable=W0611
# pylint: disable=C0103

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.v1.auth import auth_models
from app.v1.category import category_models
from app.v1.recipe import recipe_models

app = create_app(config_name='development')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
