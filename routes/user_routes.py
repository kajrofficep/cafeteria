# routes/user_routes.py

from flask import Blueprint, request, jsonify
from models.user_model import User, db
# Create a Blueprint named 'user'
user_bp = Blueprint('user', __name__)

# Define a route for creating a user
@user_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    # Extract data from the request
    username = data.get('username')
    full_name = data.get('full_name')
    department = data.get('department')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    # Check if the username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists!'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists!'}), 400

    # Create a new user
    new_user = User(
        username=username,
        full_name=full_name,
        department=department,
        email=email,
        phone=phone
    )
    new_user.set_password(password)  # Hash the password

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully!'}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(user_list)