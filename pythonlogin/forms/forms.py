from ast import Sub
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DataRequired
from wtforms.validators import DataRequired

# Name Form
class NamerForm(FlaskForm):
    name = StringField('What\'s your name?')
    submit = SubmitField('Submit')