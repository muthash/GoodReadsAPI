from flask import Blueprint, request, jsonify
from flask.views import MethodView


from app.auth.model import User, users

auth = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterUser(MethodView):
    """Method to Register a new user"""
    def post(self):
        """Endpoint to login a user"""
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        email = request.json.get('email', None)
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        emails = [user.email for user in users]
        if email in emails:
            response = {'message': 'User already exists. Please login'}
            return jsonify(response), 409
        
        user = User(email, username, password)
        users.append(user)
        return jsonify({'message': 'Account created successfully'}), 201


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))