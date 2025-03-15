# routes/protected_routes.py

from flask import Blueprint, jsonify
from flask_login import login_required, current_user

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected')
@login_required  # This ensures only logged-in users can access the route
def protected_route():
    return jsonify({"message": f"Hello, {current_user.username}! This is a protected route."})