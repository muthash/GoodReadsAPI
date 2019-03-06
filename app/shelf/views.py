from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView

from app.shelf.model import BookShelf, store

shelf = Blueprint('shelf', __name__, url_prefix='')

class ShelfManipulation(MethodView):
    @jwt_required
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        title = request.json.get('title', None)
        genre = request.json.get('genre', None)
        status = request.json.get('status', None) 
        current_user = get_jwt_identity()

        book = BookShelf(title, genre, status, current_user)
        store.append(book)
        return jsonify({'message': 'Book entry created successfully'}), 201

shelf.add_url_rule('/books', view_func=ShelfManipulation.as_view('books'))
