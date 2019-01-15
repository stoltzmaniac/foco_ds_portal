from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import DateField


class TickerForm(FlaskForm):
    ticker = StringField()
    start_date = DateField('DatePicker', format='%Y-%m-%d')
    end_date = DateField('DatePicker', format='%Y-%m-%d')
