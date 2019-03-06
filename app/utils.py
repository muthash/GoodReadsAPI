import re

from flask import jsonify
from webargs import fields, validate
from usernames import is_safe_username

user_args = {
        "email": fields.Str(required=True, validate=validate.Email()),
        "username": fields.Str(required=True, validate=validate.Length(min=3)),
        "password": fields.Str(required=True, validate=validate.Length(min=8)),
    }

def normalize_email(email):
    """Lowercase the domain part of the email"""
    email_part = email.split('@')
    domain = email_part[1].lower()
    email = email_part[0]+'@'+domain
    return email

def remove_white_spaces(user_input):
    """Maximum number os spaces between words should be one"""
    strip_text = user_input.strip()
    return re.sub(r'\s+', ' ', strip_text)


def check_username(username):
    name = remove_white_spaces(username)
    if not is_safe_username(name):
        response = {'message': "The username you provided is not allowed, " +
                               "please try again but with a different name."}
        return jsonify(response), 400

    regex = re.compile('^[a-zA-Z0-9_]{3,}$')
    res = re.match(regex, str(username))
    if not res:
        response = {'message': "The Username should contain atleast four " +
                               "alpha-numeric characters. The optional " +
                               "special character allowed is _ (underscore)."}
        return jsonify(response), 400