""" Check for errors in input submitted by user """

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
