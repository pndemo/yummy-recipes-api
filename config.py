""" Configuration specifications for testing, development and production environments """

class Config(object):
    """Parent configurations."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = 'hdjHD&*JDMDRS^&ghdD67dJHD%efgGHJDm877$$6&mbd#@bbdFGhj'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/yummydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    """Testing configurations."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/yummydb_test'
    DEBUG = True

class TestingInvalidConfig(TestingConfig):
    """Testing invalid credentials."""
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/yummydb_tests'

class DevelopmentConfig(Config):
    """Development configurations."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configurations."""
    DEBUG = False
    TESTING = False

# pylint: disable=C0103

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'testing_invalid': TestingInvalidConfig,
    'production': ProductionConfig,
}
