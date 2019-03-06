""" The create_app function wraps the creation of a new Flask object, and
    returns it after it's loaded up with configuration settingsusing app.config
"""
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager


from instance.config import app_config

jwt = JWTManager()

def create_app(config_name):
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    jwt.init_app(app)

    from app.auth.views import auth
    from app.shelf.views import shelf

    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {'roles': user.role}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.email

    app.register_blueprint(auth)
    app.register_blueprint(shelf)

    return app