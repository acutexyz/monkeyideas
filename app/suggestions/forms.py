from flask_wtf import Form
from wtforms.fields import SelectField
from wtforms.validators import DataRequired

class SuggestForm(Form):
    idea_id = SelectField('Which idea do want to share', validators=[DataRequired()], coerce=int)