from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Form, validators , TextAreaField,BooleanField,RadioField


class SolveAssignment(FlaskForm):
    
    choice = RadioField(choices=[('a1' , 'a1') , ('a2' , 'a2'), ('a3' , 'a3'), ('a4' , 'a4')])
    submit = SubmitField('Submit')


class DescriptionAssignment(FlaskForm):
    pass

class AddAssignment(FlaskForm):
    pass
  

class UpdateAssignment(FlaskForm):
    pass

class DeleteAssignment(FlaskForm):
    pass
