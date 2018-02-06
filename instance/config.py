""" Configuration specifications for testing, development, staging and production environments """

import os

class Config(object):
    """ Parent configurations. """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('HOST_USERNAME')
    MAIL_PASSWORD = os.getenv('HOST_PASSWORD')

class TestingConfig(Config):
    """ Testing configurations. """
    DEBUG = True
    TESTING = True
    SECRET = 'jhdsj%jkej$8jhjdhdjh^&kjdhdjhhdg#63KJhjejhe*hege'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/yummydb_test'

class DevelopmentConfig(Config):
    """ Development configurations. """
    DEBUG = True

class StagingConfig(Config):
    """ Staging configurations. """
    DEBUG = True

class ProductionConfig(Config):
    """ Production configurations. """
    TESTING = False

# pylint: disable=C0103

app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
