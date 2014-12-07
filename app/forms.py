from flask_wtf import Form
from wtforms.fields import (StringField, PasswordField, 
							TextAreaField, BooleanField)
from wtforms.ext.sqlalchemy.fields import (QuerySelectField, 
										   QuerySelectMultipleField)
from wtforms.validators import (DataRequired, Email, 
								Length, URL, ValidationError)
from app.models import Profession, Field, IdeaStatus, Monkey


def professions():
    return Profession.query


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), 
                             Length(min=6, max=20)])
    fullname = StringField('Full name', validators=[DataRequired(), 
                           Length(min=5, max=100)])
    about = TextAreaField('Tell about yourself', 
                          validators=[DataRequired(), 
                          Length(min=20, max=200)])
    profession_id = QuerySelectField('Profession', 
                                     validators=[DataRequired()], 
                                     get_label='name', 
                                     query_factory=professions)
    is_public = BooleanField('Allow others see you?', default=False)
    
    def validate_email(self, field):
    	"""Checks uniqueness of email
    	"""
    	if Monkey.query.filter_by(email=field.data).count() > 0:
    		raise ValidationError('This email has been already registered')
    

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


def fields():
    return Field.query


def idea_statuses():
    return IdeaStatus.query
    

class IdeaForm(Form):
    title = StringField('Title', validators=[DataRequired(), 
                        Length(min=5, max=80)])
    body = TextAreaField('Description', validators=[DataRequired()])
    fields = QuerySelectMultipleField(validators=[DataRequired()], 
                                      get_label='name', 
                                      query_factory=fields)
    is_public = BooleanField('Is publicly accessible?', 
                             validators=[DataRequired()])
    status_id = QuerySelectField('Idea status', validators=[DataRequired()], 
                                 get_label='name', 
                                 query_factory=idea_statuses)
    

class JoinRequestForm(Form):
    message = TextAreaField('Message', validators=[DataRequired(), 
                            Length(min=5, max=200)])
    

class SuggestForm(Form):
    idea_id = QuerySelectField('Which idea do you want to share', 
                               validators=[DataRequired()], get_label='title')
