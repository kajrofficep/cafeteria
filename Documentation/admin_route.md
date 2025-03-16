To allow an admin to view and edit any user's profile in a single route, you can create a dedicated route for admin access. This route will allow admins to:

View any user's profile details by providing the user's id or username.

Edit any user's profile details (including role, if needed).

Here’s how you can implement this:

Step 1: Add Admin Profile Route
Create a new file routes/admin_routes.py:

python
Copy
# routes/admin_routes.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.user_model import User, db

admin_bp = Blueprint('admin', __name__)

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
Step 2: Register the Admin Blueprint
In your app.py, register the admin_bp Blueprint:

python
Copy
# app.py

from flask import Flask
from flask_login import LoginManager
from config.conf import Config
from models.user_model import db
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.admin_routes import admin_bp  # Import the admin Blueprint

app = Flask(__name__)

# Load the configuration
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(admin_bp)  # Register the admin Blueprint

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
Step 3: Update the User Model
Ensure your User model has the is_admin method to check if the current user is an admin:

python
Copy
# models/user_model.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='user')  # Add a role field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'
Step 4: Test the Admin Profile Route
1. Login as Admin
Send a POST request to /login to log in as an admin:

bash
Copy
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin_password"}'
Response:

json
Copy
{
  "message": "Login successful!",
  "user_id": 1
}
2. View a User's Profile
Send a GET request to /admin/profile/<user_id> to view a user's profile:

bash
Copy
curl http://127.0.0.1:5000/admin/profile/2
Response:

json
Copy
{
  "username": "test_user",
  "full_name": "Test User",
  "department": "Engineering",
  "email": "test@example.com",
  "phone": "1234567890",
  "role": "user"
}
3. Update a User's Profile
Send a PUT request to /admin/profile/<user_id> to update a user's profile:

bash
Copy
curl -X PUT http://127.0.0.1:5000/admin/profile/2 \
-H "Content-Type: application/json" \
-d '{"full_name": "Updated Name", "email": "updated@example.com", "role": "moderator"}'
Response:

json
Copy
{
  "message": "User profile updated successfully!"
}
4. Verify Updated Profile
Send another GET request to /admin/profile/<user_id> to verify the updated details:

bash
Copy
curl http://127.0.0.1:5000/admin/profile/2
Response:

json
Copy
{
  "username": "test_user",
  "full_name": "Updated Name",
  "department": "Engineering",
  "email": "updated@example.com",
  "phone": "1234567890",
  "role": "moderator"
}
Key Features
Admin-Only Access:

The route checks if the current user is an admin using the is_admin method.

Non-admin users receive a 403 Forbidden response.

Flexible Updates:

Admins can update specific fields (e.g., only email or only role) without needing to provide all fields.

Role Management:

Admins can update the role field to promote or demote users.

Error Handling:

If the target user is not found, the API returns a 404 Not Found error.

Notes
Security:

Ensure that only admins can access this route by properly validating the current_user.role.

Use HTTPS in production to protect sensitive data.

Testing:

Test the route thoroughly to ensure it handles all edge cases (e.g., invalid user IDs, missing fields).

This implementation provides a clean and secure way for admins to manage user profiles in your Flask application. Let me know if you need further assistance! 😊