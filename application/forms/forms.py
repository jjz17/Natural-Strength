from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InlineButtonWidget(object):
    def __init__(self, class_=None):
        self.class_ = class_

# Name Form
class NamerForm(FlaskForm):
    name = StringField('What\'s your name?')
    submit = SubmitField('Submit')