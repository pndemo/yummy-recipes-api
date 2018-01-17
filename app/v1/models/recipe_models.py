""" Recipe module models."""

from app import db
from app.v1.models.category_models import Category
from app.v1.utils.mixins import BaseMixin, TimestampMixin

# pylint: disable=W0703
# pylint: disable=E1101

class Recipe(BaseMixin, TimestampMixin, db.Model):
    """Define the 'Recipe' model mapped to database table 'recipes'."""

    __tablename__ = 'recipes'

    recipe_name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(800), nullable=False)
    directions = db.Column(db.String(2000), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))

    def __init__(self, recipe_name, ingredients, directions, category_id):
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.directions = directions
        self.category_id = category_id

    def __repr__(self):
        return "<Recipe: {}>".format(self.recipe_name)
