""" Forms related with user account. """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Required
from wtforms.fields.html5 import DateField
from backend.web.database_api import UserInsertManager, UserFindManager
from flask import session


class RegistrationForm(FlaskForm):
    """
    Class which initializes forms related with user's registration.
    """

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    birthday = DateField('Date of Birth', format='%Y-%m-%d', validators=[Required()])
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Sign Up')

    # the 'username' arguments coming from the form, thats why i use it by this way
    def validate_username(self, username): # convention name function by flask 
        user = UserFindManager.find_user('username', username.data)
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email): 
        user = UserFindManager.find_user('email', email.data)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """
    Class which initializes forms related with user's log-in.
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """
    Class which initializes forms related with user's username update.
    """

    username = StringField('Username')
    submit_update = SubmitField('Update')


class ChangePasswordForm(FlaskForm):
    """
    Class which initializes forms related with change password process.
    """

    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit_change_password = SubmitField('Change Password')


class DeleteAccountForm(FlaskForm):
    """
    Class which initializes forms related with account's deletion.
    """

    submit_deletion = SubmitField('Yes')