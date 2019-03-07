from flask import Blueprint, request, jsonify
from flask.views import MethodView
from webargs.flaskparser import use_kwargs
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token


from app.models import User
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

        user = User.query.filter_by(email=email).first()
        if user:
            response = {'message': 'User already exists, Please login'}
            return jsonify(response), 409
        
        try:
            user = User(email=email, username=username, password=password)
            user.save()
            return jsonify({'message': 'Account created successfully'}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 401

class LoginUser(MethodView):
    """Method to login a user"""
    def post(self):
        """Endpoint to login a user"""
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400

        email_input = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email_input or not password:
            return jsonify({"message": "Missing email or password"}), 400
        
        email = normalize_email(email_input)
        try:
            user = User.query.filter_by(email=email).first()
            print(user.email)
            if user and user.password_is_valid(password):
                response = {
                    'message': 'Login successfull',
                    'access_token': create_access_token(identity=user.id)
                }
                return jsonify(response), 200
            else:
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return jsonify(response), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 401


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
auth.add_url_rule('/login', view_func=LoginUser.as_view('login'))