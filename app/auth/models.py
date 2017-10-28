""" Auth module models."""

from datetime import datetime, timedelta
import jwt
from app import create_app, db
from flask_bcrypt import Bcrypt

# pylint: disable=C0103
# pylint: disable=W0703

app = create_app('development')

class User(db.Model):
    """Define the 'User' model mapped to database table 'users'."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), \
            onupdate=db.func.current_timestamp())

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def __repr__(self):
        return "<User: {}>".format(self.email)

    def check_password(self, password):
        """Check if password is valid"""
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save to database table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete from database table"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def generate_token(user_id):
        """Generate user token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode user token"""
        try:
            payload = jwt.decode(token, app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Sorry, this token has expired."
        except jwt.InvalidTokenError:
            return "Sorry, this token is invalid."
