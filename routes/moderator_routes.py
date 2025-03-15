# routes/moderator_routes.py

from flask import Blueprint, jsonify
from decorators.decorators import role_required

moderator_bp = Blueprint('moderator', __name__)

@moderator_bp.route('/moderator')
@role_required('moderator')  # Only moderators can access this route
def moderator_dashboard():
    return jsonify({"message": "Welcome to the moderator dashboard!"})