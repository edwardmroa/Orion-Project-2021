from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,  IntegerField, SelectField, DateField
#from wtforms.fields.html5 import DecimalField, EmailField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

class RegistroComprador(FlaskForm):
    cedula = StringField('Cédula', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su cédula"})
    nombreCompleto = StringField('Nombre completo', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su nombre completo"})
    sexo = SelectField(u'Sexo', choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('NoBinario', 'Prefiero no decirlo')])
    fechaNacimiento = DateField('Fecha de nacimiento',format='%Y-%m-%d' , validators=[DataRequired(message='No dejar vacío, completar')])
    direccion = StringField('Direccion', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su direccion de residencia"})
    ciudad = StringField('Ciudad', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su direccion de residencia"})
    username = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su usuario"})
    password = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su contraseña"})
