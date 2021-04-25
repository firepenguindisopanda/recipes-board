from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo, Email


class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('email', validators=[InputRequired(), Email()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Confirm Password')
    submit = SubmitField('Confirm', render_kw={'class': 'btn waves-effect waves-light white-text green darken-2 white-text'})

class LogIn(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light green darken-2 white-text '})