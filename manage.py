""" Manage migrations """

# pylint: disable=W0611
# pylint: disable=C0103

import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.v1 import models

app = create_app(config_name='development')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def create():
    """ Command for creating main and testing databases. """
    os.system('createdb yummydb')
    os.system('createdb yummydb_test')
    print('Main and testing databases created')

@manager.command
def drop():
    """ Command for dropping main and testing databases. """
    os.system('psql -c "DROP DATABASE IF EXISTS yummydb"')
    os.system('psql -c "DROP DATABASE IF EXISTS yummydb_test"')
    print('Main and testing databases dropped')

if __name__ == '__main__':
    manager.run()
