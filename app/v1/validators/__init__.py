""" Check for errors in input submitted by user """

import re
from flask import jsonify

def data_validator(messages):
    """
    Returns True if all fields contain valid data, otherwise False if any field contains
    invalid data
    """

    for key, value in messages.items():
        if value != 'Valid':
            return False
    return True

def validate_title(title):
    """ Returns True if a valid title is provided """
    title = re.sub(' +', ' ', title.strip())
    regexp = re.compile(r"^[a-zA-Z0-9-' ]*$")
    if regexp.search(title):
        return True
    return False
