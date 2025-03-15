# routes/admin_routes.py

from flask import Blueprint, jsonify
from decorators.decorators import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@role_required('admin')  # Only admins can access this route
def admin_dashboard():
    return jsonify({"message": "Welcome to the admin dashboard!"})