""" Model mixin classes for auth, category and recipe modules """

from app import db

# pylint: disable=C0103
# pylint: disable=E1101

class BaseMixin(object):
    """ Define the 'BaseModel' mapped to all database tables. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save(self):
        """Save to database table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete from database table"""
        db.session.delete(self)
        db.session.commit()

class TimestampMixin(object):
    """ Database logging of data manipulation timestamps. """

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), \
            onupdate=db.func.current_timestamp())
