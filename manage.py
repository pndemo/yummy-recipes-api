""" Manage migrations """

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.auth import models
from app.category import models
from app.recipe import models

# pylint: disable=C0103

app = create_app(config_name='development')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
