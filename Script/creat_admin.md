This script, create_admin.py, is designed to create an admin user in your Flask application's database. It ensures that only one admin user exists and handles password hashing for security. Below is a detailed description of how the script works:

1. Import Dependencies
python
Copy
from app import app, db
from models.user_model import User
app: The Flask application instance.

db: The SQLAlchemy database instance.

User: The User model, which represents the user table in the database.

2. Define the create_admin_user Function
python
Copy
def create_admin_user():
This function is responsible for creating an admin user in the database.

3. Set Up Application Context
python
Copy
with app.app_context():
Flask requires an application context to interact with the database and other app-specific features.

The with app.app_context(): block ensures that the script runs within the Flask application context.

4. Check if an Admin User Already Exists
python
Copy
admin = User.query.filter_by(username='admin').first()
if admin:
    print("Admin user already exists!")
    return
The script queries the database to check if a user with the username 'admin' already exists.

If an admin user exists, it prints a message and exits the function to avoid creating a duplicate.

5. Create a New Admin User
python
Copy
admin = User(
    username='admin',
    full_name='Admin User',
    department='Administration',
    email='admin@example.com',
    phone='1234567890',
    role='admin'  # Set the role to 'admin'
)
A new User object is created with the following attributes:

username: 'admin'

full_name: 'Admin User'

department: 'Administration'

email: 'admin@example.com'

phone: '1234567890'

role: 'admin' (to designate this user as an admin)

6. Hash the Password
python
Copy
admin.set_password('admin_password')  # Hash the password
The set_password method (defined in the User model) hashes the plain-text password ('admin_password') using werkzeug.security.generate_password_hash.

The hashed password is stored in the password_hash field of the User model.

7. Add the Admin User to the Database
python
Copy
db.session.add(admin)
db.session.commit()
The new admin user is added to the database session.

The session is committed to save the changes to the database.

8. Print a Success Message
python
Copy
print("Admin user created successfully!")
If the admin user is created successfully, a confirmation message is printed.

9. Run the Script
python
Copy
if __name__ == '__main__':
    create_admin_user()
The script checks if it is being run directly (not imported as a module).

If so, it calls the create_admin_user function to execute the logic.

How to Use the Script
Save the Script:
Save the script as create_admin.py in your project directory.

Run the Script:
Execute the script using Python:

bash
Copy
python create_admin.py
Expected Output:

If the admin user does not exist:

Copy
Admin user created successfully!
If the admin user already exists:

Copy
Admin user already exists!
Verify the Admin User:
You can verify the admin user by querying the database:

python
Copy
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print(f"Admin user found: {admin.username}, Role: {admin.role}")
Key Features of the Script
Prevents Duplicate Admin Users:

The script checks if an admin user already exists before creating a new one.

Password Hashing:

The password is securely hashed before being stored in the database.

Database Interaction:

The script uses SQLAlchemy to interact with the database, ensuring proper database operations.

Flask Application Context:

The script runs within the Flask application context, ensuring access to the app and database.

Example Use Case
Initial Setup:
When deploying your Flask application for the first time, you can use this script to create an initial admin user.

Adding Admins:
If you need to add additional admin users, you can modify the script or create a similar script for other roles.

Notes
Password Security:
Always use a strong password for admin accounts. Avoid hardcoding passwords in production scripts; use environment variables or secure input methods instead.

Database Configuration:
Ensure that your database is properly configured and accessible before running the script.

Let me know if you need further clarification or enhancements! 😊