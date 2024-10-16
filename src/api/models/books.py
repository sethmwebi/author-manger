from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from api.utils.database import db


# Define the Book model
class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    def __init__(self, title, year, author_id=None):
        self.title = title
        self.year = year
        self.author_id = author_id

    # Method to add book to the database
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


# Define the schema for serializing the Book model
class BookSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = Book
        load_instance = True
        sqla_session = db.session

    id = auto_field(dump_only=True)
    title = auto_field(required=True)
    year = auto_field(required=True)
    author_id = fields.Integer()
