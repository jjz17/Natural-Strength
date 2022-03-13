from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import sqlalchemy as db
from sqlalchemy import text
import re
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from user import User
from base import Session
from user_metrics import UserMetrics
from datetime import date

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jiajia2002'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute(
        #     'SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        # # Fetch one record and return result
        # account = cursor.fetchone()

        db_session = Session()
        user = db_session.query(User) \
            .filter((User.username == username) & (User.password == password))

        # If account exists in accounts table in out database
        if user.count() == 1:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0].id
            session['username'] = user[0].username
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute(
                'INSERT INTO users (`username`, `password`, `email`) VALUES (%s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# Home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# Profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# Profile update page, only accessible for loggedin users
@app.route('/update', methods=['GET', 'POST'])
def update():
    # Check if user is loggedin
    if 'loggedin' in session:
        id = session['id']



        # Create a new session
        db_session = Session()



        # Output message if something goes wrong...
        msg = ''
        account = None
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            birth_date = request.form['birth_date']
            # weight = request.form['weight']
            # squat = request.form['squat']
            # bench = request.form['bench']
            # deadlift = request.form['deadlift']
            email = request.form['email']

            # # Check if account exists using MySQL
            # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute(
            #     f'SELECT * FROM accounts WHERE id = {id}')
            # account = cursor.fetchone()

            # Validation checks
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            # elif not re.match(r'^\+?(0|[1-9]\d*)$', birth_date):
                # msg = 'Birth date must be a valid date in the form MM/DD/YYYY'
            # elif not re.match(r'^(0*[1-9][0-9]*(\.[0-9]+)?|0+\.[0-9]*[1-9][0-9]*)$', weight):
            #     msg = 'Weight must be a positive number'
            # elif not re.match(r'^(0*[1-9][0-9]*(\.[0-9]+)?|0+\.[0-9]*[1-9][0-9]*)$', squat):
            #     msg = 'Squat must be a positive number'
            # elif not re.match(r'^(0*[1-9][0-9]*(\.[0-9]+)?|0+\.[0-9]*[1-9][0-9]*)$', bench):
            #     msg = 'Bench must be a positive number'
            # elif not re.match(r'^(0*[1-9][0-9]*(\.[0-9]+)?|0+\.[0-9]*[1-9][0-9]*)$', deadlift):
            #     msg = 'Deadlift must be a positive number'
            else:
                # Account doesnt exists and the form data is valid, now update data into accounts table
                # cursor.execute(
                #     f'UPDATE accounts SET username = \'{username}\', password = \'{password}\', birth_date = 1999-10-10, weight = {weight}, squat = {squat}, bench = {bench}, deadlift = {deadlift}, email = \'{email}\' WHERE id = {id};')
                # mysql.connection.commit()
                user = db_session.query(User).get(id)
                user.username = username
                user.password = password
                user.birth_date = birth_date
                user.email = email
                db_session.commit()
                db_session.close()
                msg = 'You have successfully updated!'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'

        # Show the update form with message (if any)
        return render_template('update.html', msg=msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/sql')
def sql():
    user = 'root'
    password = 'jiajia2002'
    database = 'pythonlogin'
    engine = db.create_engine(f'mysql+pymysql://{user}:{password}@localhost:3306/{database}')

    # result = engine.execute(
    #     text(
    #         "SELECT id FROM accounts ORDER BY RAND();"
    #     )
    # )

    result = engine.execute(
        text(
            "SELECT * FROM users;"
        )
    )

    result_as_list = result.fetchall()

    # return str(result.first()[0])
    return result_as_list[0]['username']


@app.route('/plot/<int:points>', methods=['GET'])
def plot(points):
    title = 'Randomly Generated Scatterplot'
    plot = plot_points(points)
    return render_template('plot.html', title=title, plot=plot)


def plot_points(points):
    """Generate a plot with a varying number of randomly generated points
    Args:
    points (int): a number of points to plot
    Returns: An svg plot with <points> data points
    """
    # data for plotting
    data = np.random

    data = np.random.rand(points, 2)

    fig = Figure()
    FigureCanvas(fig)

    ax = fig.add_subplot(111)

    ax.scatter(data[:,0], data[:,1])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'There are {points} data points!')
    ax.grid(True)

    img = io.StringIO()
    fig.savefig(img, format='svg')
    #clip off the xml headers from the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    
    return svg_img

@app.route('/chart/weight', methods=['GET'])
def chart_weight():
    title = 'Randomly Generated Scatterplot'
    plot = plot_points2(2)
    return render_template('plot.html', title=title, plot=plot)


def plot_points2(points):
    """Generate a plot with a varying number of randomly generated points
    Args:
    points (int): a number of points to plot
    Returns: An svg plot with <points> data points
    """

    fig = Figure()
    FigureCanvas(fig)

    ax = fig.add_subplot(1, 1, 1)

    # 2 - extract a session
    session = Session()

    # 3 - extract all users
    users = session.query(User).all()
    # print(users)
    ids = [user.id for user in users]

    user_metrics = session.query(UserMetrics) \
    .filter(UserMetrics.user_id == 1) \
#     .all()

    dates = [user_metric.date for user_metric in user_metrics]
    weights = [user_metric.weight for user_metric in user_metrics]

    ax.plot(dates, weights)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'There are {points} data points!')
    ax.grid(True)

    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig.suptitle('Horizontally stacked subplots')
    # x = data[:, 0]
    # y = data[:, 1]
    # ax1.plot(x, y)
    # ax2.plot(x, -y)

    img = io.StringIO()
    fig.savefig(img, format='svg')
    # clip off the xml headers from the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]

    return svg_img


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000)
