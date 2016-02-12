from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo

class RegistrationForm(Form):
    username = TextField('username', [InputRequired()])
    password = PasswordField(
            'password', [
                InputRequired(),
                EqualTo('confirm', message='passwords must match')
            ]
    )
    confirm = PasswordField('confirm password', [InputRequired()])

class LoginForm(Form):
    username = TextField('username', [InputRequired()])
    password = PasswordField('password', [InputRequired()])
