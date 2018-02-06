""" Settings and function used to send emails to users """

from flask_mail import Mail, Message
from app import create_app

# pylint: disable=C0103
# pylint: disable=W0703

app = create_app('development')
mail = Mail(app)

def send_mail(user, subject, text):
    """ Return True if email successfully sent, otherwise return False """
    msg = Message(subject, sender='hckalii2018@gmail.com', \
	        recipients=[user.email])
    msg.body = text
    mail.send(msg)
    return True
