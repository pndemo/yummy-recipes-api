""" Input data validation for registration, login and password_reset views """

import re
from validate_email import validate_email
from app.v1.models.auth_models import User

def validate_username(value, register=False):
    """
    Returns 'Valid' if the username provided by user is valid, otherwise an appropriate error
    message is returned.
    """
    regexp = re.compile(r"^\w{5,80}$")
    if not value:
        message = 'Please enter username.'
    elif not regexp.search(value):
        message = 'Please enter a valid username. Username can only contain 5-80 \
alphanumeric and underscore characters.'
    else:
        if register and (User.query.filter_by(username=value).first()):
            message = 'This username is already taken.'
        else:
            message = 'Valid'
    return message

def validate_user_email(value, register=False):
    """
    Returns 'Valid' if the email address provided by user is valid, otherwise an appropriate error
    message is returned.
    """
    if not value:
        message = 'Please enter email address.'
    elif not validate_email(value):
        message = 'Please enter a valid email address.'
    else:
        if register and (User.query.filter_by(email=value).first()):
            message = 'This email address is already registered.'
        else:
            message = 'Valid'
    return message

def validate_password(value):
    """
    Returns 'Valid' if password provided by user is valid, otherwise an appropriate error message
    is returned
    """
    if not value:
        message = 'Please enter password.'
    elif not len(value) >= 8:
        message = 'Password must be at least 8 characters.'
    else:
        message = 'Valid'
    return message

def validate_confirm_password(value, password):
    """
    Returns 'Valid' if confirmation password provided by user is valid, otherwise an appropriate
    error message is returned
    """
    message = validate_password(value)
    if message == 'Valid':
        if value != password:
            message = 'This password does not match the one entered.'
        else:
            message = 'Valid'
    return message
