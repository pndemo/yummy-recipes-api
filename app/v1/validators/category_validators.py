""" Input data validation for category views """

from app.v1.models.category_models import Category
from app.v1.validators import validate_title

def validate_category_name(value, user_id, category_id=None):
    """
    Returns 'Valid' if category name is valid and category with similar category name
    has not been created by specific user or is related to specific category id related
    to specific user
    """
    if not value:
        return 'Please enter category name.'
    elif not validate_title(value):
        return 'Please enter a valid category name.'
    else:
        categories = Category.query.filter_by(user_id=user_id)
        for category in categories:
            if category.user_id == user_id and category.category_name.lower() == \
                    value.lower():
                if category_id and category.category_id == category_id:
                    return 'Valid'
                return 'A category with this category name is already available.'
    return 'Valid'
