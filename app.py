from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required
from datetime import timedelta

from models.user_model import db, User, Meal
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from routes.protected_routes import protected_bp
from routes.moderator_routes import moderator_bp
from routes.profile_routes import profile_bp  # Import the profile Blueprint
from routes.admin_routes import admin_bp  # Import the admin Blueprint
from routes.meal_routes import meal_bp  # Import the meal Blueprint


from views.user_views import list_users
from flask_migrate import Migrate
app = Flask(__name__)

### Configuration load.
# Import Config class from config folder conf.py . Database Configuration configuration
from config.conf import Config
# Load the configuration
app.config.from_object(Config)
# Set session lifetime (e.g., 30 minutes)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


# Initialize the database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)
###########################################
# Register the Blueprint
app.register_blueprint(user_bp)
# app.register_blueprint(user_bp, url_prefix='/api')
#This would make all routes in the user_bp Bluepoint accessible under the /api prefix:
#POST /api/create_user
#GET /api/users
#If no prefix is specified, the routes are accessible directly:
#POST /create_user
#GET /users
#############################################
app.register_blueprint(auth_bp)
app.register_blueprint(protected_bp)
app.register_blueprint(moderator_bp)
app.register_blueprint(profile_bp)  # Register the profile Blueprint
app.register_blueprint(admin_bp)  # Register the admin Blueprint
app.register_blueprint(meal_bp)  # Register the meal Blueprint



# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route to render the user list view
@app.route('/show_users')
def show_users():
    return list_users()

#@app.route('/profile')
#@login_required
#def profile():
#    return f"Hello, {current_user.username}!"

@app.route('/')
def homepage():
    # You can pass variables to the template using the render_template function
    message = "Hello World farjad!"
    additional_info = "This is a Flask app with Jinja templating."
    return render_template('index.html', message_ver_homepage=message,additional_info_var_hompepage=additional_info)

# # Create the database tables
# with app.app_context():
#     db.create_all()
#     print("Database tables created successfully!")


if __name__ == '__main__':
    app.run(debug=True)