# routes/meal_routes.py

from datetime import datetime, date, timedelta, time  # Import date here
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user_model import Meal, db

meal_bp = Blueprint('meal', __name__)

def is_within_time_limit(meal_type, current_time):
    """
    Check if the current time is within the allowed time limit for the given meal type.
    """
    if meal_type == 'breakfast' and current_time >= time(7, 0):  # After 7 AM
        return False
    elif meal_type == 'lunch' and current_time >= time(11, 0):  # After 11 AM
        return False
    elif meal_type == 'dinner' and current_time >= time(14, 0):  # After 2 PM
        return False
    return True

@meal_bp.route('/meals', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def meals():
    if request.method == 'GET':
        # Get today's date and the next 3 days
        today = date.today()
        dates = [today + timedelta(days=i) for i in range(4)]  # Today + next 3 days

        # Fetch meals for the current user for these dates
        user_meals = Meal.query.filter(
            Meal.user_id == current_user.id,
            Meal.meal_date.in_(dates)
        ).order_by(Meal.meal_date).all()

        # Pass the date object to the template
        return render_template('meals.html', dates=dates, meals=user_meals, date=date, timedelta=timedelta)

    elif request.method == 'POST':
        # Handle meal updates
        meal_date_str = request.form.get('meal_date')
        breakfast = request.form.get('breakfast') == 'on'
        lunch = request.form.get('lunch') == 'on'
        dinner = request.form.get('dinner') == 'on'
        breakfast_rate = int(request.form.get('breakfast_rate', 100))  # Default rate: 100
        lunch_rate = int(request.form.get('lunch_rate', 150))  # Default rate: 150
        dinner_rate = int(request.form.get('dinner_rate', 200))  # Default rate: 200

        # Convert meal_date_str to a date object
        meal_date = datetime.strptime(meal_date_str, '%Y-%m-%d').date()
        current_date = date.today()
        current_time = datetime.now().time()

        # Check if the meal date is within the allowed range (today + next 3 days)
        if meal_date < current_date or meal_date > current_date + timedelta(days=3):
            flash("You can only add or update meals for today and the next 3 days.", "error")
            return redirect(url_for('meal.meals'))

        # Check if the meal date is today
        if meal_date == current_date:
            # Check time limits for each meal type
            if breakfast and not is_within_time_limit('breakfast', current_time):
                flash("Breakfast can only be added or updated before 7 AM.", "error")
                return redirect(url_for('meal.meals'))
            if lunch and not is_within_time_limit('lunch', current_time):
                flash("Lunch can only be added or updated before 11 AM.", "error")
                return redirect(url_for('meal.meals'))
            if dinner and not is_within_time_limit('dinner', current_time):
                flash("Dinner can only be added or updated before 2 PM.", "error")
                return redirect(url_for('meal.meals'))

        # Check if a meal entry already exists for the given date
        meal = Meal.query.filter_by(user_id=current_user.id, meal_date=meal_date).first()

        if meal:
            # Update the existing meal
            meal.breakfast = breakfast
            meal.lunch = lunch
            meal.dinner = dinner
            meal.breakfast_rate = breakfast_rate
            meal.lunch_rate = lunch_rate
            meal.dinner_rate = dinner_rate
        else:
            # Create a new meal entry
            meal = Meal(
                user_id=current_user.id,
                meal_date=meal_date,
                breakfast=breakfast,
                lunch=lunch,
                dinner=dinner,
                breakfast_rate=breakfast_rate,
                lunch_rate=lunch_rate,
                dinner_rate=dinner_rate
            )

        # Calculate the total cost
        meal.calculate_total_cost()

        # Add and commit to the database
        db.session.add(meal)
        db.session.commit()

        flash("Meal updated successfully!", "success")
        return redirect(url_for('meal.meals'))