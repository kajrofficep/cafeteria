To allow a logged-in user to view their profile details and update their profile, you can create dedicated routes in your Flask application. Below is a step-by-step guide to implement this functionality.

Step 1: Add Profile Routes
Create a new file routes/profile_routes.py to handle profile-related functionality:

python
Copy
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
Step 2: Register the Profile Blueprint
In your app.py, register the profile_bp Blueprint:

python
Copy
# app.py

from flask import Flask
from flask_login import LoginManager
from config.conf import Config
from models.user_model import db
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp  # Import the profile Blueprint

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
app.register_blueprint(profile_bp)  # Register the profile Blueprint

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
Step 3: Test the Profile Routes
1. Login as a User
Send a POST request to /login to log in as a user:

bash
Copy
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "test_user", "password": "test_password"}'
You’ll receive a response like:

json
Copy
{
  "message": "Login successful!",
  "user_id": 1
}
2. View Profile Details
Send a GET request to /profile to view the logged-in user's profile details:

bash
Copy
curl http://127.0.0.1:5000/profile
You’ll receive a response like:

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
3. Update Profile Details
Send a PUT request to /profile/update to update the logged-in user's profile details:

bash
Copy
curl -X PUT http://127.0.0.1:5000/profile/update \
-H "Content-Type: application/json" \
-d '{"full_name": "Updated Name", "email": "updated@example.com"}'
You’ll receive a response like:

json
Copy
{
  "message": "Profile updated successfully!"
}
4. Verify Updated Profile
Send another GET request to /profile to verify the updated details:

bash
Copy
curl http://127.0.0.1:5000/profile
You’ll receive a response like:

json
Copy
{
  "username": "test_user",
  "full_name": "Updated Name",
  "department": "Engineering",
  "email": "updated@example.com",
  "phone": "1234567890",
  "role": "user"
}
Step 4: Explanation of the Code
@login_required:

This decorator ensures that only logged-in users can access the profile routes.

If a user is not logged in, Flask-Login will redirect them to the login page (or return a 401 Unauthorized error).

current_user:

This is a proxy provided by Flask-Login that represents the currently logged-in user.

You can access the user's attributes (e.g., current_user.username, current_user.email) directly.

Updating Profile:

The update_profile route allows the user to update specific fields (full_name, department, email, phone).

Only the fields provided in the request are updated.

Database Commit:

After updating the user's details, the changes are committed to the database using db.session.commit().

Step 5: Enhancements (Optional)
Password Update:
Add a route to allow users to update their password:

python
Copy
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
Input Validation:
Validate the input data (e.g., check if the email is valid, ensure the phone number is in the correct format).

Error Handling:
Add error handling for cases where the database update fails.

Summary
View Profile: The /profile route allows logged-in users to view their profile details.

Update Profile: The /profile/update route allows logged-in users to update their profile details.

Security: The @login_required decorator ensures that only authenticated users can access these routes.

This implementation provides a clean and secure way for users to manage their profiles in your Flask application. Let me know if you need further assistance! 😊