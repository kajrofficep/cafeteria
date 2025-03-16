# routes/admin_routes.py

from flask import Blueprint, jsonify, request
from decorators.decorators import role_required
from flask_login import login_required, current_user
from models.user_model import User, db
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@role_required('admin')  # Only admins can access this route
def admin_dashboard():
    return jsonify({"message": "Welcome to the admin dashboard!"})


@admin_bp.route('/admin/profile/<int:user_id>', methods=['GET', 'PUT'])
@login_required  # Ensure the user is logged in
def admin_profile(user_id):
    # Check if the current user is an admin
    if not current_user.is_admin():
        return jsonify({"message": "Unauthorized access. Admin privileges required."}), 403

    # Fetch the target user by user_id
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({"message": "User not found."}), 404

    if request.method == 'GET':
        # Return the target user's profile details
        return jsonify({
            "username": target_user.username,
            "full_name": target_user.full_name,
            "department": target_user.department,
            "email": target_user.email,
            "phone": target_user.phone,
            "role": target_user.role
        })

    elif request.method == 'PUT':
        data = request.get_json()

        # Update the target user's profile details
        if 'full_name' in data:
            target_user.full_name = data['full_name']
        if 'department' in data:
            target_user.department = data['department']
        if 'email' in data:
            target_user.email = data['email']
        if 'phone' in data:
            target_user.phone = data['phone']
        if 'role' in data:
            target_user.role = data['role']  # Allow updating the role

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "User profile updated successfully!"})