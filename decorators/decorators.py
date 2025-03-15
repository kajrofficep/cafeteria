# decorators.py

from functools import wraps
from flask import jsonify
from flask_login import current_user

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                return jsonify({"message": "Unauthorized access."}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator