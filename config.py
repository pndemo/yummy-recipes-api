""" Configuration specifications for testing, development and production environments """

class Config(object):
    """Parent configurations."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = 'hdjHD&*JDMDRS^&ghdD67dJHD%efgGHJDm877$$6&mbd#@bbdFGhj'
    SQLALCHEMY_DATABASE_URI = 'postgresql://yummyadmin:ecclipse@localhost:5432/yummydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    """Testing configurations."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/yummydb_test'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://yummyadmin:ecclipse@localhost:5432/yummydb_test'
    DEBUG = True

class TestingInvalidConfig(Config):
    """Testing invalid credentials."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://yummyadmin:eclipse@localhost:5432/yummydb_test'
    DEBUG = True

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
