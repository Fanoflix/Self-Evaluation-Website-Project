from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Form, validators , TextAreaField, BooleanField, RadioField, SelectField
from myproject.models import Courses

class SolveAssignment(FlaskForm):
    pass


class DescriptionAssignment(FlaskForm):
    pass

class AddAssignment(FlaskForm):
    assignment_name = StringField('Name:', [ validators.Required() ]) 
    difficulty = SelectField('Difficulty:', choices = [('Beginner', 'Beginner'), ('intermediate', 'intermediate'), ('Expert', 'Expert')]) 
    

class DeleteAssignment(FlaskForm):
    submit = SubmitField("Delete Assignment")

