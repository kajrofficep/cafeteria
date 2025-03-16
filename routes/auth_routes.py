# routes/auth_routes.py

from flask import Blueprint, request, jsonify, redirect, url_for,render_template
from flask_login import login_user, logout_user, current_user
from models.user_model import User, db

auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#
#     # Fetch the user
#     user = User.query.filter_by(username=username).first()
#
#     # Check if the user exists and the password is correct
#     if user and user.check_password(password):
#         login_user(user)  # Log the user in
#         return jsonify({"message": "Login successful!", "user_id": user.id})
#     else:
#         return jsonify({"message": "Invalid username or password."}), 401
#
# @auth_bp.route('/logout', methods=['POST'])
# def logout():
#     logout_user()  # Log the user out
#     return jsonify({"message": "Logout successful!"})

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Fetch the user
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            login_user(user)  # Log the user in
            return render_template('profile.html', user=user)  # Redirect to profile page
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('login'))  # Redirect to the login page