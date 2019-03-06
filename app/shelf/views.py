from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from flask.views import MethodView

from app.models import Shelf

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

        try:
            book = Shelf(title, genre, status, current_user)
            book.save()
            return jsonify({'message': 'Book entry created successfully'}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 401

    @jwt_optional
    def get(self, shelf_id):
        if shelf_id is None:
            books = Shelf.get_all()
            if books:
                res = [book.serialize() for book in books]
                response = {'Available books': res}
                return jsonify(response), 200
            else:
                response = {'message': 'There are no book entries currently'}
            return jsonify(response), 202
        
        book = Shelf.query.filter_by(id=shelf_id).first()
        if not book:
            response = {'message': f'The book with id {shelf_id} is not available'}
            return jsonify(response), 404
        response = {'book details': book.serialize()}
        return jsonify(response), 200

    @jwt_required
    def patch(self, shelf_id):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        status = request.json.get('status', None)
        current_user = get_jwt_identity()

        book = Shelf.query.filter_by(id=shelf_id).first()
        if not book:
            return jsonify({"message": f'The book with id {shelf_id} is not available'}), 400
        
        if book.id != current_user:
            return jsonify({"message": 'You are forbidden from editing this entry'}), 403
        
        try:
            book.update(status)
            response = {'message': 'Book status updated successfully', 
                        'book details': book.serialize()}
            return jsonify(response), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 401
        

shelf_view = ShelfManipulation.as_view('books')
shelf.add_url_rule('', view_func=shelf_view, methods=['POST', ])
shelf.add_url_rule('', defaults={'shelf_id': None}, view_func=shelf_view, methods=['GET', ])
shelf.add_url_rule('/<int:shelf_id>', view_func=shelf_view , methods=['GET', 'PATCH'])
