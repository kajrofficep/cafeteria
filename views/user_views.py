# views/user_views.py

from flask import render_template
from models.user_model import User

def list_users():
    # Fetch all users from the database
    users = User.query.all()
    # Render the 'users.html' template with the user data
    return render_template('users.html', users=users)