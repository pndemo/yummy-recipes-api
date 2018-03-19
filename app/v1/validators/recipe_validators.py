""" Input data validation for recipe views """

from app.v1.models.recipe_models import Recipe
from app.v1.validators import validate_title

def validate_recipe_name(value, category_id, recipe_id=None):
    """
    Returns 'Valid' if recipe name is valid and recipe with similar recipe name
    has not been created under specific category or is related to specific recipe id related
    to specific category
    """
    if not value:
        return 'Please enter recipe name.'
    elif not validate_title(value):
        return 'Please enter a valid recipe name.'
    else:
        recipes = Recipe.query.filter_by(category_id=category_id)
        for recipe in recipes:
            if recipe.category_id == category_id and recipe.recipe_name.lower() == \
                    value.lower():
                if recipe_id and recipe.id == recipe_id:
                    return 'Valid'
                return 'A recipe with this recipe name is already available.'
    return 'Valid'

def validate_ingredients(value):
    """
    Returns 'Valid' if ingredient field is not empty
    """
    if not value:
        return 'Please enter ingredients.'
    return 'Valid'

def validate_directions(value):
    """
    Returns 'Valid' if directions field is not empty
    """
    if not value:
        return 'Please enter directions.'
    return 'Valid'
