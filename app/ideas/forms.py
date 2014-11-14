from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired
  
class IdeaForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Description', validators=[DataRequired()])
    fields = SelectMultipleField('Fields', validators=[DataRequired()], coerce=int)
    is_public = BooleanField('Is publicly accessible?', validators=[DataRequired()])
    status_id = SelectField('What phase is your idea in?', validators=[DataRequired()], coerce=int)