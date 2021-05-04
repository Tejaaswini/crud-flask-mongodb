from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SubmitField

class CreateTask(FlaskForm):
    title = TextField('TODO Title')
    tododesc = TextField('TODO Description')
    create = SubmitField('Create')

class DeleteTask(FlaskForm):
    key = TextField('TODO ID')
    title = TextField('TODO Title')
    delete = SubmitField('Delete')

class UpdateTask(FlaskForm):
    key = TextField('TODO ID')
    tododesc = TextField('TODO Description')
    update = SubmitField('Update')

class ResetTask(FlaskForm):
    reset = SubmitField('Reset')
