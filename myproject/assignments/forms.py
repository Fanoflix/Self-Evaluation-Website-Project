from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Form, validators , TextAreaField, BooleanField, RadioField, SelectField
from myproject.models import Courses

class SolveAssignment(FlaskForm):
    pass


class DescriptionAssignment(FlaskForm):
    pass

class AddAssignment(FlaskForm):
    assignment_name = StringField('Assignment Name:', [ validators.Required() ]) 
    difficulty = SelectField('Select Difficulty:', choices = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Expert', 'Expert')]) 
    

class DeleteAssignment(FlaskForm):
    submit = SubmitField("Delete Assignment")

class SubmitAssignment(FlaskForm):
    review = TextAreaField('Review: ', [ validators.Required() ])
    rating =  SelectField('Select Rating:', [ validators.Required() ] , choices = [(1 ,'1-Star'), (2 ,'2-Star'), (3 ,'3-Star'),  (4 ,'4-Star'),  (5 ,'5-Star')]) 
    submit = SubmitField("Submit Review")

