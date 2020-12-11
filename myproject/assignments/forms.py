from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Form, validators , TextAreaField, BooleanField, RadioField, SelectField
from myproject.models import Courses

class SolveAssignment(FlaskForm):
    pass


class DescriptionAssignment(FlaskForm):
    pass

class AddAssignment(FlaskForm):
    assignment_name = StringField('Name:', [ validators.Required() ]) 
    difficulty = SelectField('Difficulty:', choices = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Expert', 'Expert')]) 
    course = SelectField('Course: ', choices = [(course.id, course.course_name) for course in Courses.query.all()])



class AddSolution(FlaskForm):
    # assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    # question_id = db.Column(db.Integer)
    # assignment = db.relationship('Assignments', backref = 'assignments') # Backref
    # choice1 = db.Column(db.Text)
    # choice2 = db.Column(db.Text)
    # choice3 = db.Column(db.Text)
    # choice4 = db.Column(db.Text)
    # answer = db.Column(db.Text)
    pass

class DeleteAssignment(FlaskForm):
    pass


