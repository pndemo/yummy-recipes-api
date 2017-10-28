""" Running application configuration """

from app import create_app

# pylint: disable=C0103

config_name = 'development'
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
