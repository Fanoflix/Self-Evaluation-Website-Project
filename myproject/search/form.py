from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

class Searching(FlaskForm):
    searched = StringField()
    submit = SubmitField()