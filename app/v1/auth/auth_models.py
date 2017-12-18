""" Auth module models."""

from datetime import datetime, timedelta
import jwt
from app import db
from flask_bcrypt import Bcrypt

# pylint: disable=C0103
# pylint: disable=W0703

class User(db.Model):
    """Define the 'User' model mapped to database table 'users'."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), \
            onupdate=db.func.current_timestamp())
    categories = db.relationship('Category', order_by='Category.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def __repr__(self):
        return "<User: {}>".format(self.email)

    def check_password(self, password):
        """Check if password is valid"""
        return Bcrypt().check_password_hash(self.password, password)

    def hash_password(self, password):
        """Encrypt password before storage"""
        return Bcrypt().generate_password_hash(password).decode()

    def save(self):
        """Save to database table"""
        db.session.add(self)
        db.session.commit()

    def encode_token(self, user_id):
        """Generate user token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                'hdjHD&*JDMDRS^&ghdD67dJHD%efgGHJDm877$$6&mbd#@bbdFGhj',
                algorithm='HS256'
            )
        except Exception as exp:
            return str(exp)

    @staticmethod
    def decode_token(token):
        """Decode user token"""
        revoked_token = RevokedToken.query.filter_by(token=str(token)).first()
        if not revoked_token:
            try:
                payload = jwt.decode(
                    token,
                    'hdjHD&*JDMDRS^&ghdD67dJHD%efgGHJDm877$$6&mbd#@bbdFGhj',
                    algorithms=['HS256']
                )
                return payload['sub']
            except jwt.ExpiredSignatureError:
                return 'Sorry, this token has expired.'
            except jwt.InvalidTokenError:
                return 'Sorry, this token is invalid.'
        else:
            return 'Sorry, this token is invalid.'

class RevokedToken(db.Model):
    """Define the 'RevokedToken' model mapped to database table 'revoked_tokens'."""

    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    revoked_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.revoked_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    def save(self):
        """Save to database table"""
        db.session.add(self)
        db.session.commit()
