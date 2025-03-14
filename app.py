from flask import Flask, render_template
app = Flask(__name__)

### Configuration load.
# Import Config class from config folder conf.py . Database Configuration configuration
from config.conf import Config
# Load the configuration
app.config.from_object(Config)


@app.route('/')
def homepage():
    # You can pass variables to the template using the render_template function
    message = "Hello World farjad!"
    additional_info = "This is a Flask app with Jinja templating."
    return render_template('index.html', message_ver_homepage=message,additional_info_var_hompepage=additional_info)


if __name__ == '__main__':
    app.run()