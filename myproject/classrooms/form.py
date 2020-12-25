from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Form, validators , TextAreaField, BooleanField, RadioField, SelectField
# from myproject.models import *

class AddClassroom(FlaskForm):
    class_name = StringField('Class Name:', [ validators.Required() ])
    submit = SubmitField("Add Class")
 
class AddClassroomAssignments(FlaskForm):
    pass

class StudentJoinClassroom(FlaskForm):
    submit = SubmitField("Join Class")