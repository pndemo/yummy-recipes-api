""" Input data validation for registration, login and password_reset views """

from validate_email import validate_email

def validate_user_email(value):
    """
    Returns 'Valid' if the email address provided by user is valid, otherwise an appropriate error
    message is returned.
    """
    if not value:
        message = 'Please enter email address.'
    elif not validate_email(value):
        message = 'Please enter a valid email address.'
    else:
        message = 'Valid'
    return message

def validate_password(value):
    """
    Returns 'Valid' if password provided by user is valid, otherwise an appropriate error message
    is returned
    """
    if not value:
        message = 'Please enter password'
    elif not len(value) >= 8:
        message = 'Password must be at least 8 characters.'
    else:
        message = 'Valid'
    return message
