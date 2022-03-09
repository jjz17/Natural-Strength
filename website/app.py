from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/user/<usr>')
def user_home(usr):
    return f'Welcome to your home, {usr}!'


@app.route('/input')
def user_input():
    pass


@app.route('/practice')
def practice():
    return str(datetime.now())
    # return render_template('practice.html', time=time)


if __name__ == '__main__':
    app.run()