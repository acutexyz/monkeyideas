from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    fullname = StringField('Full name', validators=[DataRequired(), Length(min=5)])
    about = TextAreaField('Tell about yourself', validators=[DataRequired(), Length(min=20, message="Tell about yourself at least 20 characters ;)")])
    profession_id = SelectField('Profession', validators=[DataRequired()], coerce=int)
    is_public = BooleanField('Allow others see you?', default=False)
    
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])