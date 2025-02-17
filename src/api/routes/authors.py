from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from api.models.authors import Author, AuthorSchema
from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with

author_routes = Blueprint("author_routes", __name__)


@author_routes.route("/", methods=["POST"])
@jwt_required()
def create_route():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author = author_schema.load(data)

        author.create()

        result = author_schema.dump(author)
        return response_with(resp.SUCCESS_201, value={"author": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@author_routes.route("/", methods=["GET"])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=["first_name", "last_name", "id"])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route("/<int:author_id>", methods=["GET"])
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get_or_404(id)
    get_author.first_name = data["first_name"]
    get_author.last_name = data["last_name"]
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def modify_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get(id)

    if not get_author:
        return response_with(
            resp.SERVER_ERROR_404, message=f"Author with id {id} not found"
        )

    if data.get("first_name"):
        get_author.first_name = data["first_name"]
    if data.get("last_name"):
        get_author.last_name = data["last_name"]
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_author(id):
    get_author = Author.query.get_or_404(id)
    db.session.delete(get_author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)
