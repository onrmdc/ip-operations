from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    input_ip_address = StringField('input_ip_address', validators=[DataRequired(), Length(min=7, max=18)])