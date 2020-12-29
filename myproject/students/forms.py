from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, Form, validators , TextAreaField,BooleanField

class SignUp(FlaskForm):

    fname = StringField('First Name:', [ validators.Required() ]) 
    lname = StringField('Last Name:', [ validators.Required() ]) 
    uname = StringField('User Name:', [validators.Required()])
    email = StringField('Email:', [ validators.Required() ]) 
    password1 = PasswordField('Password:',[ validators.Required() , ])
    password2 = PasswordField('Retype Password:',[ validators.Required() ])
    submit = SubmitField('Sign Up') 

class LogIn(FlaskForm):

    email = StringField('Email:', [ validators.Required() ]) 
    password = PasswordField('Password', [ validators.Required() ])
    submit = SubmitField('Log In')

class ProfileTab(FlaskForm):
    uname = StringField()
    fname = StringField()
    lname = StringField()
    bio = TextAreaField()
    submit = SubmitField('SAVE')

class AccountTab(FlaskForm):

    password1 = PasswordField([ validators.Required() ])
    password2 = PasswordField([ validators.Required() ])
    password3 = PasswordField([ validators.Required() ])
    submit = SubmitField('Change Password') 

class PrivacyTab(FlaskForm):

    displayRank = BooleanField( [ validators.Required() ])
    displayStats = BooleanField( [ validators.Required() ])
    submit = SubmitField('SAVE')

class DeactivateTab(FlaskForm):
    password = PasswordField([ validators.Required() ])
    submit = SubmitField('Close Account')
