# routes/meal_routes.py

from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from models.user_model import Meal, db

meal_bp = Blueprint('meal', __name__)

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

        return render_template('meals.html', dates=dates, meals=user_meals)

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

        return redirect(url_for('meal.meals'))  # Redirect back to the meals page