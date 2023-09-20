from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistroForm(FlaskForm):
    nombreRegistro = StringField('nombreRegistro', validators=[DataRequired(), Length(max=50)])
    emailRegistro = StringField('emailRegistro', validators=[DataRequired(), Email()])
    passwordRegistro = PasswordField('passwordRegistro', validators=[DataRequired(), Length(min=8, max=15)])
    submit = SubmitField('submit')