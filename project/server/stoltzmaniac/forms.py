from flask_wtf import FlaskForm
from wtforms import FileField


class FileUploadForm(FlaskForm):
    file = FileField("Upload CSV")
