from app import db
from flask_bcrypt import Bcrypt

class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    books = db.relationship('Shelf', backref='owner', order_by='Shelf.id',
                                cascade="all, delete-orphan", lazy=True)

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

class Shelf(db.Model):

    __tablename__ = 'shelf'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False, unique=True)
    genre = db.Column(db.String(256), nullable=False, unique=True)
    status = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, genre, status, user_id):
        self.title = title
        self.genre = genre
        self.status = status
        self.user_id = user_id
    
    def serialize(self):
        return {
            'book_id': self.id,
            'title': self.title,
            'genre':  self.genre,
            'status': self.status,
            'created_by': self.owner.username
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, status):
        self.status = status
        db.session.commit()

    @staticmethod
    def get_all():
        return Shelf.query.all()
    
    def __repr__(self):
        return '<Book %r>' % self.title
