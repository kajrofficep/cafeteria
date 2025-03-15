# routes/profile_routes.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.user_model import User, db

profile_bp = Blueprint('profile', __name__)

# Route to view profile details
@profile_bp.route('/profile', methods=['GET'])
@login_required  # Ensure the user is logged in
def view_profile():
    # Return the current user's profile details
    return jsonify({
        "username": current_user.username,
        "full_name": current_user.full_name,
        "department": current_user.department,
        "email": current_user.email,
        "phone": current_user.phone,
        "role": current_user.role
    })

# Route to update profile details
@profile_bp.route('/profile/update', methods=['PUT'])
@login_required  # Ensure the user is logged in
def update_profile():
    data = request.get_json()

    # Update the user's profile details
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    if 'department' in data:
        current_user.department = data['department']
    if 'email' in data:
        current_user.email = data['email']
    if 'phone' in data:
        current_user.phone = data['phone']

    # Commit changes to the database
    db.session.commit()

    return jsonify({"message": "Profile updated successfully!"})

@profile_bp.route('/profile/update_password', methods=['PUT'])
@login_required
def update_password():
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({"message": "New password is required."}), 400

    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully!"})

#  This below route only profile route update everything
# # routes/profile_routes.py
#
# from flask import Blueprint, request, jsonify
# from flask_login import login_required, current_user
# from models.user_model import User, db
#
# profile_bp = Blueprint('profile', __name__)
#
# @profile_bp.route('/profile', methods=['GET', 'PUT'])
# @login_required  # Ensure the user is logged in
# def profile():
#     if request.method == 'GET':
#         # Return the current user's profile details
#         return jsonify({
#             "username": current_user.username,
#             "full_name": current_user.full_name,
#             "department": current_user.department,
#             "email": current_user.email,
#             "phone": current_user.phone,
#             "role": current_user.role
#         })
#
#     elif request.method == 'PUT':
#         data = request.get_json()
#
#         # Update profile details
#         if 'full_name' in data:
#             current_user.full_name = data['full_name']
#         if 'department' in data:
#             current_user.department = data['department']
#         if 'email' in data:
#             current_user.email = data['email']
#         if 'phone' in data:
#             current_user.phone = data['phone']
#
#         # Update password if provided
#         if 'new_password' in data:
#             new_password = data['new_password']
#             if not new_password:
#                 return jsonify({"message": "New password cannot be empty."}), 400
#             current_user.set_password(new_password)
#
#         # Commit changes to the database
#         db.session.commit()
#
#         return jsonify({"message": "Profile updated successfully!"})