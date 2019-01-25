from datetime import date as dt
from datetime import timedelta

from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import DateField


class TickerForm(FlaskForm):
    ticker = StringField(default="AAPL,MSFT")
    start_date = DateField("DatePicker", format="%Y-%m-%d", default=dt.today)
    end_date = DateField("DatePicker", format="%Y-%m-%d", default=dt.today)
