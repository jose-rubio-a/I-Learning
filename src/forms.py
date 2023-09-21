from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistroForm(FlaskForm):
    nombreRegistro = StringField('nombreRegistro', validators=[DataRequired(), Length(max=50)])
    emailRegistro = StringField('emailRegistro', validators=[DataRequired(), Email()])
    passwordRegistro = PasswordField('passwordRegistro', validators=[DataRequired(), Length(min=8, max=15)])
    submit = SubmitField('submit')

class EditarForm(FlaskForm):
    nombre = StringField('nombre', validators=[DataRequired(), Length(max=50)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=15)])
    submit = SubmitField('submit')