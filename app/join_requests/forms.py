from flask_wtf import Form
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired

class JoinRequestForm(Form):
    message = TextAreaField('Message', validators=[DataRequired()])