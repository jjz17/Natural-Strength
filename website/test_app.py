from flask import Flask, render_template, request, flash
from matplotlib import dates
import sqlalchemy as db
from sqlalchemy import text
import io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from user import User
from base import Session
from user_metrics import UserMetrics
from datetime import date

app = Flask(__name__)
app.secret_key = 'abc'


@app.route('/')
def home():
    return 'Home'


@app.route('/hello')
def index():
    flash('What is your height in inches?')
    return render_template('index2.html')


@app.route('/convert', methods=['POST', 'GET'])
def greeter():
    height_cm = round(int(request.form['height_input']) * 2.54, 2)
    message = f'Your height in cm is {height_cm}'
    flash(message=message)
    return render_template('index2.html')


@app.route('/sql')
def sql():
    user = 'root'
    password = 'jiajia2002'
    database = 'pythonlogin'
    engine = db.create_engine(
        f'mysql+pymysql://{user}:{password}@localhost:3306/{database}')

    result = engine.execute(
        text(
            "SELECT id FROM accounts ORDER BY RAND();"
        )
    )
    return str(result.first()[0])


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

    ax = fig.add_subplot(1, 1, 1)

    # ax.scatter(data[:, 0], data[:, 1])

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
