from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, TextAreaField, SelectMultipleField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Email, Length, NumberRange, URL, AnyOf, NoneOf
from app.models import Profession, Field, IdeaStatus

def professions():
    return Profession.query

class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    fullname = StringField('Full name', validators=[DataRequired(), Length(min=5)])
    about = TextAreaField('Tell about yourself', validators=[DataRequired(), Length(min=20, message="Tell about yourself at least 20 characters ;)")])
    profession_id = QuerySelectField('Profession', validators=[DataRequired()], get_label='name', query_factory=professions)
    is_public = BooleanField('Allow others see you?', default=False)
    
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

def fields():
    return Field.query

def idea_statuses():
    return IdeaStatus.query
    
class IdeaForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Description', validators=[DataRequired()])
    fields = QuerySelectMultipleField(validators=[DataRequired()], get_label='name', query_factory=fields)
    is_public = BooleanField('Is publicly accessible?', validators=[DataRequired()])
    status_id = QuerySelectField('Idea status', validators=[DataRequired()], get_label='name', query_factory=idea_statuses)
    
class JoinRequestForm(Form):
    message = TextAreaField('Message', validators=[DataRequired()])
    
class SuggestForm(Form):
    idea_id = QuerySelectField('Which idea do you want to share', validators=[DataRequired()], get_label='title')
