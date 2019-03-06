from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from flask.views import MethodView

from app.shelf.model import BookShelf, store

shelf = Blueprint('shelf', __name__, url_prefix='/books')

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

    @jwt_optional
    def get(self, shelf_id):
        if shelf_id is None:
            books = [book.serialize() for book in store]
            if books:
                response = {'Available books': books}
                return jsonify(response), 200
            else:
                response = {'message': 'There are no book entries currently'}
            return jsonify(response), 202
        
        books = [book.serialize() for book in store if shelf_id == book.id]
        if not books:
            response = {'message': f'The book with id {shelf_id} is not available'}
            return jsonify(response), 404
        response = {'book details': books}
        return jsonify(response), 200

    @jwt_required
    def patch(self, shelf_id):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        status = request.json.get('status', None)
        current_user = get_jwt_identity()

        book = [book for book in store
                     if shelf_id == book.id and current_user==book.email]
        if not book:
            return jsonify({"message": "The action is Forbidden"}), 403
        
        index = store.index(book[0])
        store[index].status = status

        response = {'message': 'Book status updated successfully', 'book details': store[index].serialize()}
        return jsonify(response), 200
        

shelf_view = ShelfManipulation.as_view('books')
shelf.add_url_rule('', view_func=shelf_view, methods=['POST', ])
shelf.add_url_rule('', defaults={'shelf_id': None}, view_func=shelf_view, methods=['GET', ])
shelf.add_url_rule('/<int:shelf_id>', view_func=shelf_view , methods=['GET', 'PATCH'])
