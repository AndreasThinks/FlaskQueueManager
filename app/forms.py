from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class AddTask(Form):
    name = TextField('name', validators = [Required()])

class AddType(Form):
    type = TextField('type', validators = [Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AddType, self).__init__(*args, **kwargs)

class LoginForm(Form):
    username = TextField('Username', validators = [Required()])
    password = TextField('password', validators = [Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(LoginForm, self).__init__(*args, **kwargs)