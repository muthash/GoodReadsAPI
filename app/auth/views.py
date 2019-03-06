from flask import Blueprint, request, jsonify
from flask.views import MethodView
from webargs.flaskparser import use_kwargs


from app.auth.model import User, users
from app.utils import user_args, normalize_email, check_username

auth = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterUser(MethodView):
    """Method to Register a new user"""
    @use_kwargs(user_args, locations=("json",))
    def post(self, email, username, password):
        """Endpoint to login a user"""
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        
        email = normalize_email(email)

        if check_username(username):
            return check_username(username)

        emails = [user.email for user in users]
        if email in emails:
            response = {'message': 'User already exists, Please login'}
            return jsonify(response), 409
        
        user = User(email, username, password)
        users.append(user)
        return jsonify({'message': 'Account created successfully'}), 201


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))