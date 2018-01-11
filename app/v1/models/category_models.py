""" Category module models."""

from app import db
from app.v1.models.auth_models import User
from app.v1.utils.mixins import BaseMixin, TimestampMixin

# pylint: disable=W0703
# pylint: disable=E1101

class Category(BaseMixin, TimestampMixin, db.Model):
    """Define the 'Category' model mapped to database table 'categories'."""

    __tablename__ = 'categories'

    category_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    recipes = db.relationship('Recipe', order_by='Recipe.id', cascade="all, delete-orphan")

    def __init__(self, category_name, user_id):
        self.category_name = category_name
        self.user_id = user_id

    def __repr__(self):
        return "<Category: {}>".format(self.category_name)
