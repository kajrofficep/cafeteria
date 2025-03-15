from flask import Flask, render_template
from models.user_model import db
from routes.user_routes import user_bp
from views.user_views import list_users
from flask_migrate import Migrate
app = Flask(__name__)

### Configuration load.
# Import Config class from config folder conf.py . Database Configuration configuration
from config.conf import Config
# Load the configuration
app.config.from_object(Config)



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

# Route to render the user list view
@app.route('/show_users')
def show_users():
    return list_users()

@app.route('/')
def homepage():
    # You can pass variables to the template using the render_template function
    message = "Hello World farjad!"
    additional_info = "This is a Flask app with Jinja templating."
    return render_template('index.html', message_ver_homepage=message,additional_info_var_hompepage=additional_info)


if __name__ == '__main__':
    app.run()