from app import db
from flask_bcrypt import Bcrypt

class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    # books = db.relationship('Shelf', backref='owner', order_by='Books.id',
    #                             cascade="all, delete-orphan", lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')
    
    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username
