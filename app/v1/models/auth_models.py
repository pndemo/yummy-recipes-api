""" Auth module models. """

from datetime import datetime, timedelta
import jwt
from flask_bcrypt import generate_password_hash, check_password_hash
from instance.config import Config
from app import db
from app.v1.utils.mixins import BaseMixin, TimestampMixin

# pylint: disable=W0703
# pylint: disable=E1101

class User(BaseMixin, TimestampMixin, db.Model):
    """ Define the 'User' model mapped to database table 'users'. """

    __tablename__ = 'users'

    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    categories = db.relationship('Category', order_by='Category.id', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return "<User: {}>".format(self.username)

    def check_password(self, password):
        """Check if password is valid"""
        return check_password_hash(self.password, password)

    def hash_password(self, password):
        """Encrypt password before storage"""
        return generate_password_hash(password).decode('utf-8')

    def encode_token(self, user_id):
        """Generate user token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, 'hdjHD&*JDMDRS^&ghdD67dJHD%efgGHJDm877$$6&mbd#@bbdFGhj', algorithm='HS256')
        except Exception as error:
            return str(error)

    @staticmethod
    def decode_token(token):
        """Decode user token"""
        revoked_token = RevokedToken.query.filter_by(token=str(token)).first()
        if not revoked_token:
            try:
                payload = jwt.decode(token, 'hdjHD&*JDMDRS^&ghdD67dJHD%efgGHJDm877$$6&mbd#@bbdFGhj', algorithms=['HS256'])
                return payload['sub']
            except jwt.DecodeError:
                return 'Sorry, this token could not be decoded.'
        else:
            return 'Sorry, this token is invalid.'

class RevokedToken(BaseMixin, db.Model):
    """ Define the 'RevokedToken' model mapped to database table 'revoked_tokens'. """

    __tablename__ = 'revoked_tokens'

    token = db.Column(db.String(500), unique=True, nullable=False)
    revoked_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.revoked_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
