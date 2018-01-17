""" Configuration specifications for testing, development staging and production environments """

import os

class Config(object):
    """ Parent configurations. """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    """ Testing configurations. """
    TESTING = True
    SECRET = 'hdjHD&*JDMDRS^&ghdD67dJHD%efgGHJDm877$$6&mbd#@bbdFGhj'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/yummydb_test'
    DEBUG = True

class DevelopmentConfig(Config):
    """ Development configurations. """
    DEBUG = True

class StagingConfig(Config):
    """ Staging configurations. """
    DEBUG = True

class ProductionConfig(Config):
    """ Production configurations. """
    DEBUG = False
    TESTING = False

# pylint: disable=C0103

app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
