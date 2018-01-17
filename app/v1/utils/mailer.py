""" Settings and function used to send emails to users """

import requests

URL = 'https://api.mailgun.net/v3/sandbox362fd54f9ecc4009863808af412cd1b0.mailgun.org'

API_KEY = 'key-3b5108bc69b6e4d55077afc8e4b72731'

FROM = 'Yummy Recipes Inc. <postmaster@sandbox362fd54f9ecc4009863808af412cd1b0.mailgun.org>'

def send_mail(user, subject, text):
    """ Return True if email successfully sent, otherwise return False """
    try:
        requests.post(URL, auth=("api", API_KEY), data={"from":FROM, "to":user.email, \
                "subject":subject, "text":text})
        return True
    except Exception:
        return False
