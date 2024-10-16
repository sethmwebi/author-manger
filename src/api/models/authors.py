from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from api.models.books import BookSchema
from api.utils.database import db


# Define the Author model
class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship with the Book model
    books = db.relationship("Book", backref="author", cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, books=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    # Method to add author to the database
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


# Define the schema for serializing the Author model
class AuthorSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Author
        load_instance = True
        sqla_session = db.session

    id = auto_field(dump_only=True)
    first_name = auto_field(required=True)
    last_name = auto_field(required=True)
    created = auto_field(dump_only=True)

    # Nested schema for books related to the author
    books = fields.Nested(BookSchema, many=True, only=["title", "year", "id"])
