heroku ps:scale web=1
web: waitress-serve --threads=8 --port=$PORT run:app
release: python manage.py create
release: python manage.py db initial
release: python manage.py db migrate
release: python manage.py db upgrade
