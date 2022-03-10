from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from files_lib import get_local_config_data


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    faction = SelectField('Faction', choices=get_local_config_data(section='factions'), validators=[DataRequired()], render_kw={"placeholder": "faction"})
    submit = SubmitField('Register') 

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')