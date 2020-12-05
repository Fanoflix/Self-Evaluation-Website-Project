from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Form, validators

class SignUp(FlaskForm):

    name = StringField('Username:', [ validators.Required() ]) 
    email = StringField('Email:', [ validators.Required() ]) 
    password1 = PasswordField('Password:',[ validators.Required() , ])
    password2 = PasswordField('Retype Password:',[ validators.Required() ])
    submit = SubmitField('Sign Up') 

class LogIn(FlaskForm):

    email = StringField('Email:', [ validators.Required() ]) 
    password = PasswordField('Password', [ validators.Required() ])
    submit = SubmitField('Log In')

class ShiftControl(FlaskForm):
    submit = SubmitField ('Login as Teacher')