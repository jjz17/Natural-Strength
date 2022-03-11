from flask import Flask, render_template, request, flash
import sqlalchemy as db
from sqlalchemy import text

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
    engine = db.create_engine(f'mysql+pymysql://{user}:{password}@localhost:3306/{database}',
                              # connect_args={"ssl": {"key": SQLALCHEMY_DATABASE_PEM}},
                              # echo=True,
                              )

    result = engine.execute(
        text(
            "SELECT id FROM accounts ORDER BY RAND();"
        )
    )
    return str(result.first()[0])
    return 'Hi'


if __name__ == '__main__':
    app.run()
