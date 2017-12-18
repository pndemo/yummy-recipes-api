""" Recipe module models."""

from app import db
from app.v1.category.category_models import Category

# pylint: disable=C0103
# pylint: disable=W0703

class Recipe(db.Model):
    """Define the 'Recipe' model mapped to database table 'recipes'."""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(800), nullable=False)
    directions = db.Column(db.String(2000), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), \
            onupdate=db.func.current_timestamp())

    def __init__(self, title, ingredients, directions, category_id):
        self.title = title
        self.ingredients = ingredients
        self.directions = directions
        self.category_id = category_id

    def __repr__(self):
        return "<Recipe: {}>".format(self.title)

    def save(self):
        """Save to database table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete from database table"""
        db.session.delete(self)
        db.session.commit()
