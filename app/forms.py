from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, IntegerField
from wtforms.validators import Required, length

class AddTask(Form):
    name = TextField('name', validators = [Required()])

class AddType(Form):
    type = TextField('type', validators = [Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AddType, self).__init__(*args, **kwargs)

class LoginForm(Form):
    username = TextField('Username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(LoginForm, self).__init__(*args, **kwargs)

class ReportForm(Form):
    day_from = IntegerField('Day From', validators = [Required(), length(2)])
    month_from = IntegerField('Day From', validators = [Required(), length(2)])
    year_from = IntegerField('Day From', validators = [Required(), length(4)])
    day_to = IntegerField('Day From', validators = [Required(), length(2)])
    month_to = IntegerField('Day From', validators = [Required(), length(2)])
    year_to = IntegerField('Day From', validators = [Required(), length(4)])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(ReportForm, self).__init__(*args, **kwargs)