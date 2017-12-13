""" Category module models."""

from app import db
from app.v1.auth.auth_models import User

# pylint: disable=C0103
# pylint: disable=W0703

class Category(db.Model):
    """Define the 'Category' model mapped to database table 'categories'."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), \
            onupdate=db.func.current_timestamp())
    recipes = db.relationship('Recipe', order_by='Recipe.id', cascade="all, delete-orphan")

    def __init__(self, category_name, user_id):
        self.category_name = category_name
        self.user_id = user_id

    def __repr__(self):
        return "<Category: {}>".format(self.category_name)

    def save(self):
        """Save to database table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete from database table"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """Get specific user's categories"""
        return Category.query.filter_by(user_id=user_id)
