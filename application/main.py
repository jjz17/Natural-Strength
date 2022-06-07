from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import joblib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.style import use
import numpy as np
import pandas as pd
from sqlalchemy import func
import xgboost as xgb

from datetime import date
from dateutil.relativedelta import relativedelta
import io
import re

# from application import app
# from application import forms
# from application.base import Session
# from application.user import User
# from application.user_metrics import UserMetrics, DummyUserMetrics
# from application.utils import choose_pred, copy_metrics, generate_null_metrics, handle_unit_conversion, kg_to_lbs, lbs_to_kg, metrics_kg_to_lbs

import forms
from base import Session
from user import User
from user_metrics import UserMetrics, DummyUserMetrics
from utils import choose_pred, copy_metrics, generate_null_metrics, handle_unit_conversion, kg_to_lbs, lbs_to_kg, metrics_kg_to_lbs

# Uncomment to run app through this file (main.py)
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Avoid multithreading MatPlotLib GUI error
plt.switch_backend('Agg')

# # Load in the models
squat_model = xgb.XGBRegressor()
squat_model.load_model('../models/squat.txt')
bench_model = xgb.XGBRegressor()
bench_model.load_model('../models/bench.txt')
deadlift_model = xgb.XGBRegressor()
deadlift_model.load_model('../models/deadlift.txt')

# Global variable
today = date.today()

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        db_session = Session()
        # Check exists record with matching username and password
        user_query = db_session.query(User) \
            .filter((User.username == username) & (User.password == password))
        db_session.close()
        # If user exists in users table in the database
        if user_query.count() == 1:
            user = user_query[0]
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user.id
            session['username'] = user.username
            # Toggles between STANDARD and METRIC
            session['units'] = 'STANDARD'
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # User doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('loginpage.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.clear()
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'birth_date' in request.form and 'email' in request.form and 'sex' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        birth_date = request.form['birth_date']
        email = request.form['email']
        sex = request.form['sex']

        db_session = Session()
        user_query = db_session.query(User) \
            .filter(User.username == username)

        # If user exists show error and validation checks
        if user_query.count() > 0:
            msg = 'User already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            user = User(username, password, birth_date, email, sex)
            db_session.add(user)
            db_session.commit()
            db_session.close()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('registerpage.html', msg=msg)


# Home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        session['current_page'] = 'home'
        db_session = Session()

        user_metric = db_session.query(UserMetrics) \
            .filter(UserMetrics.user_id == session['id']) \
            .order_by(UserMetrics.date.desc()) \
            .first()

        max_squat = copy_metrics(db_session.query(UserMetrics)
                                 .filter(UserMetrics.user_id == session['id'])
                                 .order_by(UserMetrics.squat.desc())
                                 .first())

        max_bench = copy_metrics(db_session.query(UserMetrics)
                                 .filter(UserMetrics.user_id == session['id'])
                                 .order_by(UserMetrics.bench.desc())
                                 .first())

        max_deadlift = copy_metrics(db_session.query(UserMetrics)
                                    .filter(UserMetrics.user_id == session['id'])
                                    .order_by(UserMetrics.deadlift.desc())
                                    .first())

        db_session.close()

        no_metrics_for_today = True
        # Check if the most recent metrics are for today
        if user_metric != None:
            if user_metric.date == today:
                no_metrics_for_today = False

            if session['units'] == 'STANDARD':
                output_unit_kg = False
            else:
                output_unit_kg = True
            conversion = handle_unit_conversion(input_unit_kg=True, output_unit_kg=output_unit_kg,
                                                user_metric=user_metric, max_squat=max_squat, max_bench=max_bench, max_deadlift=max_deadlift)
        else:
            conversion = generate_null_metrics()

        data = conversion['data']
        return render_template('homepage.html', username=session['username'].title(), no_metrics_for_today=no_metrics_for_today, last_record=data['user_metric'], max_squat=data['max_squat'], max_bench=data['max_bench'], max_deadlift=data['max_deadlift'], units=conversion['units'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Profile page, only accessible for loggedin users
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        session['current_page'] = 'profile'
        # We need all the user's info so we can display it on the profile page

        db_session = Session()
        # Select the current user's records in the databse
        user_query = db_session.query(User) \
            .filter(User.id == session['id'])
        db_session.close()
        user = user_query[0]

        # Calculate user age
        age = relativedelta(today, user.birth_date).years

        # Show the profile page with user info
        return render_template('profilepage.html', user=user, age=age)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Metrics insert page, only accessible for loggedin users
@app.route('/metrics', methods=['GET', 'POST'])
def metrics():
    # Check if user is loggedin
    if 'loggedin' in session:
        session['current_page'] = 'metrics'
        id = session['id']

        # Create a new session
        db_session = Session()

        # Output message if something goes wrong...
        msg = ''
        user = db_session.query(User).get(id)
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'weight' in request.form and 'squat' in request.form and 'bench' in request.form and 'deadlift' in request.form:
            # Create variables for easy access
            weight = request.form['weight']
            squat = request.form['squat']
            bench = request.form['bench']
            deadlift = request.form['deadlift']
            entry_date = request.form['date']

            # Convert metrics to be inserted
            if session['units'] == 'STANDARD':
                conversion = handle_unit_conversion(
                    input_unit_kg=False, output_unit_kg=True, weight=weight, squat=squat, bench=bench, deadlift=deadlift)
            else:
                conversion = handle_unit_conversion(
                    input_unit_kg=True, output_unit_kg=True, weight=weight, squat=squat, bench=bench, deadlift=deadlift)

            data = conversion['data']
            weight = data['weight']
            squat = data['squat']
            bench = data['bench']
            deadlift = data['deadlift']

            metrics_query = db_session.query(UserMetrics) \
                .filter((UserMetrics.date == today) & (UserMetrics.user == user))

            # If entry exists for this day, update it
            if metrics_query.count() == 1:
                metrics = metrics_query[0]
                metrics.weight = weight
                metrics.squat = squat
                metrics.bench = bench
                metrics.deadlift = deadlift
            # Else insert new metrics record
            else:
                metrics = UserMetrics(
                    user, weight, squat, bench, deadlift, entry_date)
                db_session.add(metrics)
            msg = 'You have successfully inserted your data!'
        elif request.method == 'POST' and ('delete_last' in request.form or 'delete_all' in request.form):
            if 'delete_last' in request.form:
                user_metric = db_session.query(UserMetrics) \
                    .filter(UserMetrics.user_id == session['id']) \
                    .order_by(UserMetrics.date.desc()) \
                    .first()
                if user_metric == None:
                    msg = 'No records remaining'
                else:
                    db_session.delete(user_metric)
                    msg = 'Last record deleted'
            else:
                db_session.query(UserMetrics) \
                    .filter(UserMetrics.user_id == session['id']).delete()
                msg = 'All records deleted'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'

        db_session.commit()
        db_session.close()
        # Show the update form with message (if any)
        return render_template('metricspage.html', msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST' and 'search' in request.form:
        search_query = request.form['search']
        return search_query
 

@app.route('/units', methods=['POST'])
def set_units():
    if request.method == 'POST' and 'units' in request.form:
        # Create variables for easy access
        units = request.form['units']
        session['units'] = units
        if session['current_page'] in {'chart_metric', 'goals'}:
            return redirect(url_for(session['current_page'], metric=session['param']))
        return redirect(url_for(session['current_page']))

# Displays the plot of the requested user metric
@app.route('/chart/<metric>', methods=['GET', 'POST'])
def chart_metric(metric):
    # Check if user is loggedin
    if 'loggedin' in session:
        session['current_page'] = 'chart_metric'
        session['param'] = metric
        title = f'Your Custom {metric.title()} Plot'
        plot = plot_metric(metric)
        return render_template('chart.html', title=title, plot=plot)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

def plot_metric(metric):
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    FigureCanvas(fig)

    db_session = Session()

    user_metrics = db_session.query(UserMetrics) \
        .filter(UserMetrics.user_id == session['id']) \
        .order_by(UserMetrics.date.asc())

    dates = [user_metric.date for user_metric in user_metrics]
    metric_list = [getattr(user_metric, metric)
                   for user_metric in user_metrics]

    # Convert metrics data to metric units to plot
    if session['units'] == 'STANDARD':
        metric_list = [kg_to_lbs(metric) for metric in metric_list]

    ax.plot(dates, metric_list)

    ax.set_xlabel('Date')

    if session['units'] == 'STANDARD':
        unit = 'Lbs'
    else:
        unit = 'Kg'
    ax.set_ylabel(f'{metric.title()} ({unit})')
    # ax.set_title(f'There are {points} data points!')
    ax.grid(True)

    # Rotate x-axis labels to fit on chart
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    # Make room for x and y labels
    plt.tight_layout()

    img = io.StringIO()
    fig.savefig(img, format='svg')
    # clip off the xml headers from the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]

    return svg_img


@app.route('/goals/<metric>', methods=['GET', 'POST'])
def goals(metric):
    # Check if user is loggedin
    if 'loggedin' in session:
        session['current_page'] = 'goals'
        session['param'] = metric
        id = session['id']

        # Create a new session
        db_session = Session()

        user_metric = db_session.query(UserMetrics) \
            .filter(UserMetrics.user_id == session['id']) \
            .order_by(UserMetrics.date.desc()) \
            .first()

        if user_metric != None:
            conversion = handle_unit_conversion(
                input_unit_kg=True, output_unit_kg=True, user_metric=user_metric)
        else:
            conversion = generate_null_metrics()

        user_metric = conversion['data']['user_metric']
        weight = user_metric.weight
        squat = user_metric.squat
        bench = user_metric.bench
        deadlift = user_metric.deadlift

        # Output message if something goes wrong...
        msg = ''
        user = db_session.query(User).get(id)

        pred = ''

        # Calculate user age
        age = relativedelta(today, user.birth_date).years

        # Determine user sex
        male = 0
        female = 0
        if user.sex == 0:
            male = 1
        elif user.sex == 1:
            female = 1
        else:
            pass

        if isinstance(user_metric, DummyUserMetrics) and user_metric.weight == None:
            pred = 'No data'
            squat_pred = 'No data'
            bench_pred = 'No data'
            deadlift_pred = 'No data'
        else:
            pred = np.float64(1.0)
            squat_input = pd.DataFrame({'Age': [age], 'BodyweightKg': [weight], 'Best3BenchKg': [
                                       bench], 'Best3DeadliftKg': [deadlift], 'Sex_F': [female], 'Sex_M': [male]})
            squat_pred = squat_model.predict(squat_input)[0]
            bench_input = pd.DataFrame({'Age': [age], 'BodyweightKg': [weight], 'Best3SquatKg': [
                                       squat], 'Best3DeadliftKg': [deadlift], 'Sex_F': [female], 'Sex_M': [male]})
            bench_pred = bench_model.predict(bench_input)[0]
            deadlift_input = pd.DataFrame({'Age': [age], 'BodyweightKg': [weight], 'Best3SquatKg': [
                                          squat], 'Best3BenchKg': [bench], 'Sex_F': [female], 'Sex_M': [male]})
            deadlift_pred = deadlift_model.predict(deadlift_input)[0]

            # Convert prediction to lbs if necessary
            if type(pred) == np.float64:
                # Handle extrapolation
                squat_pred = choose_pred(squat, squat_pred)
                bench_pred = choose_pred(bench, bench_pred)
                deadlift_pred = choose_pred(deadlift, deadlift_pred)

                pred = round(pred, 2)
                squat_pred = round(squat_pred, 2)
                bench_pred = round(bench_pred, 2)
                deadlift_pred = round(deadlift_pred, 2)
                if session['units'] == 'STANDARD':
                    pred = kg_to_lbs(pred)
                    squat_pred = kg_to_lbs(squat_pred)
                    bench_pred = kg_to_lbs(bench_pred)
                    deadlift_pred = kg_to_lbs(deadlift_pred)

            else:
                pred = 'No data'
                squat_pred = 'Nodata'
                bench_pred = 'No data'
                deadlift_pred = 'No data'

            # Convert metrics to be inserted
            if session['units'] == 'STANDARD':
                conversion = handle_unit_conversion(
                    input_unit_kg=True, output_unit_kg=False, weight=weight, squat=squat, bench=bench, deadlift=deadlift, user_metric=user_metric)
            else:
                conversion = handle_unit_conversion(
                    input_unit_kg=True, output_unit_kg=True, weight=weight, squat=squat, bench=bench, deadlift=deadlift, user_metric=user_metric)

            user_metric = conversion['data']['user_metric']

        if request.method == 'POST':
            # Create variables for easy access
            age = request.form['age']
            sex = request.form['sex']
            weight = request.form['weight']
            squat = request.form['squat']
            bench = request.form['bench']
            deadlift = request.form['deadlift']
            entry_date = request.form['date']

        return render_template('goals.html', metric=metric, pred=pred, last_record=user_metric, sp=squat_pred, bp=bench_pred, dp=deadlift_pred, units=conversion['units'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/news')
def news():
    # Check if user is loggedin
    if 'loggedin' in session:
        session['current_page'] = 'news'
        return render_template('news.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Check if user is loggedin
    if 'loggedin' in session:
        session['current_page'] = 'settings'
        id = session['id']

        # Create a new session
        db_session = Session()

        # Output message if something goes wrong...
        msg = ''
        user = None
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            birth_date = request.form['birth_date']
            email = request.form['email']
            if request.form.get('notifications'):
                notifications = 1
            else:
                notifications = 0

            # Validation checks
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            # elif not re.match(r'^\+?(0|[1-9]\d*)$', birth_date):
                # msg = 'Birth date must be a valid date in the form MM/DD/YYYY'
            else:
             # Update data into users table
                user = db_session.query(User).get(id)
                user.username = username
                user.password = password
                user.birth_date = birth_date
                user.email = email
                user.notifications = notifications
                db_session.commit()
                db_session.close()
                msg = 'You have successfully updated!'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'

        # Show the update form with message (if any)
        return render_template('settings.html', msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/about')
def about():    
    # Check if user is loggedin
    if 'loggedin' in session:
        session['current_page'] = 'about'
        return render_template('about.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


'''
--------------------Experiemental pages------------------------
'''


@app.route('/boot')
def boot():
    return render_template('homepage.html')


@app.route('/wtforms', methods=['GET', 'POST'])
def wtforms():
    name = None
    form = forms.NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('wtforms.html', name=name, form=form)


# Uncomment to run app through this file (main.py)
if __name__ == '__main__':
    app.run()
    app.run(host='0.0.0.0', port=5000)
