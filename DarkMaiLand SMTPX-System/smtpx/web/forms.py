from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email

class ComposeForm(FlaskForm):
    recipients = StringField('To', validators=[DataRequired(), Email()])
    subject = StringField('Subject')
    body = TextAreaField('Message')
    attachments = FileField('Attachments')
