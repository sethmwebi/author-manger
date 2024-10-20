from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from passlib.hash import pbkdf2_sha256 as sha256

from api.utils.database import db


# Define the User model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Method to add user to the database
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


# Define the schema for serializing the User model
class UserSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = User
        load_instance = True
        sqla_session = db.session

    id = auto_field(dump_only=True)
    username = auto_field(required=True)
    password = auto_field(required=True)
