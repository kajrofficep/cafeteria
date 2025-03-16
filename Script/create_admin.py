# create_admin.py

from app import app, db
from models.user_model import User

def create_admin_user():
    with app.app_context():
        # Check if an admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists!")
            return

        # Create a new admin user
        admin = User(
            username='farjads',
            full_name='Farjad Ullah',
            department='WEB',
            email='kmfarjadullah@gmail.com',
            phone='018299831011',
            role='admin'  # Set the role to 'admin'
        )
        admin.set_password('admin_password')  # Hash the password

        # Add the admin user to the database
        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully!")

#if __name__ == '__main__':
    #create_admin_user()
    #print('script are okey'far)