from flask_wtf import Form
from wforms.fields import StringField, PasswordField, TextAreaField, SelectField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, URL, AnyOf, NoneOf

class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    fullname = StringField('Full name', validators=[DataRequired()], Length(min=5))
    about = TextAreaField('About', validators=[DataRequired(), Length(min=20, message="Tell about yourself at least 20 characters ;)")])
    profession_id = SelectField('Profession', validators=[DataRequired()], coerce=int)
    is_public = BooleanField('Can others find you?', validators=[DataRequired()])
    facebook = StringField('Your Facebook profile url (if you have one)', validators=[URL()])
    
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class IdeaForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Description', validators=[DataRequired()])
    fields = SelectMultipleField('Fields', validators=[DataRequired()], coerce=int)
    is_public = BooleanField('Is publicly accessible?', validators=[DataRequired()])
    status_id = SelectField('What phase is your idea in?', validators=[DataRequired()], coerce=int)
    
class JoinRequestForm(Form):
    message = TextAreaField('Message', validators=[DataRequired()])
    
class SuggestForm(Form):
    idea_id = SelectField('Which idea do want to share', validators=[DataRequired()], coerce=int)
    

    