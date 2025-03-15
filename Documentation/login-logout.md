Let’s implement login and logout functionality for users in your Flask application. We’ll use Flask-Login, a popular extension for managing user sessions, to handle the login and logout process.

Step 1: Install Required Packages
Install the necessary packages:

bash
Copy
pip install flask flask-sqlalchemy flask-login
Step 2: Update the User Model
To work with Flask-Login, your User model must implement certain methods. Update your User model as follows:

python
Copy
# models/user_model.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
UserMixin: This provides default implementations for the methods required by Flask-Login, such as is_authenticated, is_active, is_anonymous, and get_id.

Step 3: Initialize Flask-Login
In your app.py, initialize Flask-Login and set up the user_loader callback:

python
Copy
# app.py

from flask import Flask
from flask_login import LoginManager
from config.conf import Config
from models.user_model import db, User

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

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
Step 4: Create Login and Logout Routes
Add routes for login and logout in a new file, routes/auth_routes.py:

python
Copy
# routes/auth_routes.py

from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, current_user
from models.user_model import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Fetch the user
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and user.check_password(password):
        login_user(user)  # Log the user in
        return jsonify({"message": "Login successful!", "user_id": user.id})
    else:
        return jsonify({"message": "Invalid username or password."}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()  # Log the user out
    return jsonify({"message": "Logout successful!"})
Step 5: Protect Routes with Login Required
You can protect routes so that only logged-in users can access them. Use the @login_required decorator from Flask-Login.

For example, let’s create a protected route:

python
Copy
# routes/protected_routes.py

from flask import Blueprint, jsonify
from flask_login import login_required, current_user

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected')
@login_required  # This ensures only logged-in users can access the route
def protected_route():
    return jsonify({"message": f"Hello, {current_user.username}! This is a protected route."})
Step 6: Register Blueprints
Register the auth_bp and protected_bp Blueprints in your app.py:

python
Copy
# app.py

from flask import Flask
from flask_login import LoginManager
from config.conf import Config
from models.user_model import db
from routes.auth_routes import auth_bp
from routes.protected_routes import protected_bp

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
app.register_blueprint(protected_bp)

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
Step 7: Test the Login and Logout Functionality
Start the Flask app:

bash
Copy
python app.py
Create a test user (if you don’t already have one):
Use a script or a route to create a test user:

python
Copy
from models.user_model import User, db

with app.app_context():
    user = User(username="test_user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()
    print("Test user created!")
Login:
Send a POST request to /login with the username and password:

bash
Copy
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "test_user", "password": "test_password"}'
If successful, you’ll receive:

json
Copy
{"message": "Login successful!", "user_id": 1}
Access Protected Route:
Send a GET request to /protected:

bash
Copy
curl http://127.0.0.1:5000/protected
If logged in, you’ll receive:

json
Copy
{"message": "Hello, test_user! This is a protected route."}
If not logged in, you’ll receive a 401 Unauthorized error.

Logout:
Send a POST request to /logout:

bash
Copy
curl -X POST http://127.0.0.1:5000/logout
You’ll receive:

json
Copy
{"message": "Logout successful!"}
Step 8: Add Session Management (Optional)
By default, Flask-Login uses cookies to manage user sessions. If you want to customize session behavior (e.g., session expiration), you can configure it in app.py:

python
Copy
from datetime import timedelta

# Set session lifetime (e.g., 30 minutes)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
Summary
Flask-Login simplifies user session management.

Login: Use login_user to log a user in.

Logout: Use logout_user to log a user out.

Protected Routes: Use @login_required to restrict access to logged-in users.

This setup provides a robust and secure way to handle user authentication in your Flask application. Let me know if you need further assistance! 😊


