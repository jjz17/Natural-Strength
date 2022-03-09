from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'abc'


@app.route('/')
def home():
    return 'Home'


@app.route('/hello')
def index():
    flash('What is your height in inches?')
    return render_template('index2.html')

@app.route('/predict', methods=['POST', 'GET'])
def greeter():
    height_cm = round(int(request.form['height_input']) * 2.54, 2)
    message = f'Your height in cm is {height_cm}'
    flash(message=message)
    return render_template('index2.html')


if __name__ == '__main__':
    app.run()
