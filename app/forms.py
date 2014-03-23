from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class AddTask(Form):
    name = TextField('name', validators = [Required()])

class AddType(Form):
    type = TextField('type', validators = [Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AddType, self).__init__(*args, **kwargs)