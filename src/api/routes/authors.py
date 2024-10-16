from flask import Blueprint, request

from api.models.authors import Author, AuthorSchema
from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with

author_routes = Blueprint("author_routes", __name__)
