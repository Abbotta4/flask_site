from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, EqualTo, Length

class MyForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    confirm = StringField('Confirm Password', [DataRequired()])
    
    def validate_name(form, field):
        if len(field.data) > 50:
            raise ValidationError('Name must be less than 50 characters')
