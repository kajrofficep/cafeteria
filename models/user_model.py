# models/user_model.py
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Hash the password
    #The set_password method is used to hash a plain-text password and store the hash in the password_hash field of the User model.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify the password
    # The check_password method is used to verify whether a provided plain-text password matches the hashed password stored in the database.
    # It uses the check_password_hash function from the werkzeug.security library to perform this verification securely.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'