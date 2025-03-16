# models/user_model.py
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='user')  # Add a role field

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

    def is_admin(self):
        return self.role == 'admin'

    def is_moderator(self):
        return self.role == 'moderator'
    
    
class Meal(db.Model):
    __tablename__ = 'meal'  # Explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User
    breakfast = db.Column(db.Boolean, default=False)  # Breakfast status
    lunch = db.Column(db.Boolean, default=False)  # Lunch status
    dinner = db.Column(db.Boolean, default=False)  # Dinner status
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # When the meal was added
    meal_date = db.Column(db.Date, default=date.today)  # Date of the meal

    # Meal rates with default values set to 0
    breakfast_rate = db.Column(db.Integer, nullable=False, default=0)
    lunch_rate = db.Column(db.Integer, nullable=False, default=0)
    dinner_rate = db.Column(db.Integer, nullable=False, default=0)

    total_cost = db.Column(db.Integer, default=0)  # Total cost of the meal

    # Relationship to User model
    user = db.relationship('User', backref=db.backref('meals', lazy=True))

    def calculate_total_cost(self):
        """
        Calculate the total cost of the meal based on the selected meals and their rates.
        """
        cost = 0
        if self.breakfast:
            cost += self.breakfast_rate
        if self.lunch:
            cost += self.lunch_rate
        if self.dinner:
            cost += self.dinner_rate
        self.total_cost = cost

    def __repr__(self):
        return f'<Meal {self.id} for {self.user.username} on {self.meal_date}>'