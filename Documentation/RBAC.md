Adding user role management to your Flask application allows you to control access to different parts of your application based on the user's role (e.g., admin, moderator, regular user). Here's how you can implement role-based access control (RBAC) in your Flask app.

Step 1: Add a Role Field to the User Model
Update your User model to include a role field. This field will store the user's role (e.g., admin, moderator, user).

python
Copy
# models/user_model.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='user')  # Add a role field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_moderator(self):
        return self.role == 'moderator'
role: This field stores the user's role. Default is 'user'.

is_admin() and is_moderator(): Helper methods to check the user's role.

Step 2: Create a Migration to Add the Role Field
If your database already exists, you need to create a migration to add the role field.

Generate a Migration:

bash
Copy
flask db migrate -m "Add role field to User model"
Apply the Migration:

bash
Copy
flask db upgrade
Step 3: Protect Routes Based on Roles
You can create a custom decorator to restrict access to routes based on the user's role.

Create a Custom Decorator
Add a new file decorators.py:

python
Copy
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
role_required(role): This decorator ensures that only users with the specified role can access the route.

Step 4: Use the Decorator in Routes
Now, you can use the role_required decorator to protect routes.

Example: Admin-Only Route
python
Copy
# routes/admin_routes.py

from flask import Blueprint, jsonify
from decorators import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@role_required('admin')  # Only admins can access this route
def admin_dashboard():
    return jsonify({"message": "Welcome to the admin dashboard!"})
Example: Moderator-Only Route
python
Copy
# routes/moderator_routes.py

from flask import Blueprint, jsonify
from decorators import role_required

moderator_bp = Blueprint('moderator', __name__)

@moderator_bp.route('/moderator')
@role_required('moderator')  # Only moderators can access this route
def moderator_dashboard():
    return jsonify({"message": "Welcome to the moderator dashboard!"})
Step 5: Register Blueprints
Register the admin_bp and moderator_bp Blueprints in your app.py:

python
Copy
# app.py

from flask import Flask
from flask_login import LoginManager
from config.conf import Config
from models.user_model import db
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.moderator_routes import moderator_bp

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
app.register_blueprint(admin_bp)
app.register_blueprint(moderator_bp)

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
Step 6: Test Role-Based Access
Create Test Users:
Create users with different roles (e.g., admin, moderator, user).

python
Copy
with app.app_context():
    admin = User(username="admin", role="admin")
    admin.set_password("admin_password")
    db.session.add(admin)

    moderator = User(username="moderator", role="moderator")
    moderator.set_password("moderator_password")
    db.session.add(moderator)

    user = User(username="user", role="user")
    user.set_password("user_password")
    db.session.add(user)

    db.session.commit()
    print("Test users created!")
Login as Admin:
Send a POST request to /login:

bash
Copy
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin_password"}'
Access the admin route:

bash
Copy
curl http://127.0.0.1:5000/admin
You should see:

json
Copy
{"message": "Welcome to the admin dashboard!"}
Login as Moderator:
Send a POST request to /login:

bash
Copy
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "moderator", "password": "moderator_password"}'
Access the moderator route:

bash
Copy
curl http://127.0.0.1:5000/moderator
You should see:

json
Copy
{"message": "Welcome to the moderator dashboard!"}
Login as Regular User:
Send a POST request to /login:

bash
Copy
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "user", "password": "user_password"}'
Try accessing the admin or moderator routes:

bash
Copy
curl http://127.0.0.1:5000/admin
curl http://127.0.0.1:5000/moderator
You should see:

json
Copy
{"message": "Unauthorized access."}
Step 7: Add More Roles (Optional)
You can add more roles (e.g., editor, viewer) by updating the role field in the User model and creating additional decorators or routes as needed.

Summary
Role Field: Add a role field to the User model to store the user's role.

Custom Decorator: Create a role_required decorator to restrict access based on roles.

Protected Routes: Use the decorator to protect routes for specific roles.

Testing: Create test users with different roles and verify access.

This setup provides a flexible and secure way to manage user roles in your Flask application. Let me know if you need further assistance! 😊