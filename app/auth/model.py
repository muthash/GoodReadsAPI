from flask_bcrypt import Bcrypt

users=[]

class User():
    """user contains an email, a username and a password"""
    def __init__(self, email, username, password, role="user"):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')
        self.role = role

    def update_password(self, password):
        self.password = Bcrypt().generate_password_hash(password).decode()
        # pw_hash = bcrypt.generate_password_hash(‘hunter2’).decode(‘utf-8’)
    
    def serialize(self):
        return {'email': self.email,
                'role': self.role
                }
    
    def make_admin(self):
        self.role = 'admin'

    def __repr__(self):
        return 'user is {}'.format(self.email)