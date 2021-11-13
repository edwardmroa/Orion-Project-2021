from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,  IntegerField, SelectField, DateField, FloatField
#from wtforms.fields.html5 import DecimalField, EmailField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, Regexp

class RegistroComprador(FlaskForm):
    cedula = StringField('Cédula', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su cédula"})
    nombreCompleto = StringField('Nombre completo', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su nombre completo"})
    sexo = SelectField(u'Sexo', choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('NoBinario', 'Prefiero no decirlo')])
    fechaNacimiento = DateField('Fecha de nacimiento',format='%Y-%m-%d' , validators=[DataRequired(message='No dejar vacío, completar')])
    direccion = StringField('Direccion', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su direccion de residencia"})
    ciudad = StringField('Ciudad', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su direccion de residencia"})
    username = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su usuario"})
    password = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su contraseña"})

class producto(FlaskForm):
    id_producto = IntegerField('ID del producto',render_kw={"placeholder":"Ingrese el ID"})
    nombre_producto = StringField('Nombre del producto',render_kw={"placeholder":"Ingrese el nombre"})
    qty = IntegerField('Cantidad disponible', render_kw={"placeholder":"Ingrese la cantidad disponible"})
    unidad = StringField('Unidades',render_kw={"placeholder":"Ingrese la unidad de empaque"})
    precio = IntegerField('Valor',render_kw={"placeholder":"Ingrese el precio del producto"})
    promocion = FloatField('Porcentaje de promoción',render_kw={"placeholder":"Ingrese el porcentaje de promoción"})
    num_ventas = IntegerField('Número total de ventas',render_kw={"placeholder":"Ingrese el número total de ventas"})
    total_ventas= IntegerField('Valor total de ventas',render_kw={"placeholder":"Ingrese el valor Total de ventas"})
    calificacion = FloatField('Calificación promedio',render_kw={"placeholder":"Ingrese la calificación Promedio"})
    aplica_descuento = SelectField('Aplica a descuento',choices=[(2, 'Seleccionar'), (1,"Si"), (0,"No")],default=2)
    acum_descontado = IntegerField('Valor acumulado descontado',render_kw={"placeholder":"Ingrese el valor acumulado descontado"})
    categoria = StringField('Categoría del producto',render_kw={"placeholder":"Ingrese la categoría del producto"})
    baja = SelectField('Dado de baja',choices=[(2, 'Seleccionar'), (1,"Si"), (0,"No")],default=2)
    listar = SubmitField( 'Listar', render_kw={"onmouseover": "listarProd()", "class":"form_boton"})
    eliminar = SubmitField( 'Eliminar', render_kw={"onmouseover": "eliminarProd()", "class":"form_boton"})
    actualizar = SubmitField( 'Actualizar', render_kw={"onmouseover": "actualizarProd()","class":"form_boton"})
    crear = SubmitField( 'Crear', render_kw={"onmouseover": "crearProd()","class":"form_boton"})

class Login(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su usuario"})
    password = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su contraseña"})

class PerfilUsuario(FlaskForm):
    cedula = StringField('Cédula', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su cédula","disabled":"true"})
    nombreCompleto = StringField('Nombre completo', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su nombre completo","disabled":"true"})
    sexo = SelectField(u'Sexo', choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('NoBinario', 'Prefiero no decirlo')], render_kw = {"disabled":"true"})
    fechaNacimiento = DateField('Fecha de nacimiento',format='%Y-%m-%d' , validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"disabled":"true"})
    direccion = StringField('Direccion', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su direccion de residencia","disabled":"true"})
    ciudad = StringField('Ciudad', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su direccion de residencia","disabled":"true"})
    username = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su usuario","disabled":"true"})
    cargo = StringField('Cargo', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite el cargo","disabled":"true"})
    rol = SelectField(u'Rol', choices=[('Super administrador', 'Super administrador'), ('Usuario interno', 'Usuario interno'), ('Usuario externo', 'Usuario externo')], render_kw = {"disabled":"true"})

class formularioLogin(FlaskForm):
    logusuario= StringField('Usuario', validators=[InputRequired(message='Este campo no puede estar vacío'), Regexp('^\w+$',message='No usar caracteres especiales')])
    logclave= PasswordField('Contraseña', validators=[InputRequired(message='Este campo no puede estar vacío'), Regexp('^\w+$',message='No usar caracteres especiales')])
    enviar = SubmitField('INICIAR SESIÓN')
    
class formularioRegistro(FlaskForm):
    regnombre = StringField('Nombre', validators=[InputRequired(message='Este campo no puede estar vacío'), Length(min=5,max=16, message = 'Este campo debe tener entre 5 y 10 caracteres'), Regexp('^[a-zA-Z0-9\s]+$',message='No usar caracteres especiales')])
    regusuario = StringField('Usuario', validators=[InputRequired(message='Este campo no puede estar vacío'), Length(min=5,max=12, message = 'Este campo debe tener entre 5 y 10 caracteres'), Regexp('^\w+$',message='No usar caracteres especiales')])
    regclave = PasswordField('Contraseña', validators=[InputRequired(message='Este campo no puede estar vacío'), Length(min=5,max=12, message = 'Este campo debe tener entre 5 y 10 caracteres'), Regexp('^\w+$',message='No usar caracteres especiales')])
    regclave2 = PasswordField('Confirmar Contraseña', validators=[InputRequired(message='Este campo no puede estar vacío'),EqualTo('regclave', message='Contraseñas deben ser iguales'), Regexp('^\w+$',message='No usar caracteres especiales')])
    registrarse = SubmitField('REGISTRATE')

class CambioPassword(FlaskForm):
    actual = PasswordField('Contraseña actual', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite su contraseña actual"})
    nueva = PasswordField('Contraseña nueva', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite la nueva contraseña"})
    confirmacion = PasswordField('Confirme su nueva contraseña', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Confirme su nueva contraseña"})
    guardar = SubmitField('GUARDAR')

class EliminarCuenta(FlaskForm):
    password = PasswordField('Confirme su contraseña', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Ingrese su contraseña actual"})
    confirmar = SubmitField('CONFIRMAR')

class ListarOperarios(FlaskForm):
    busqueda = StringField('', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Escriba la cedula del usuario interno a buscar"})
    enviar = SubmitField('Buscar')

class RegistrarOperario(FlaskForm):
    cedula = StringField('Cédula', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite la cédula"})
    nombreCompleto = StringField('Nombre completo', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite el nombre completo"})
    sexo = SelectField(u'Sexo', choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('NoBinario', 'Prefiero no decirlo')])
    fechaNacimiento = DateField('Fecha de nacimiento',format='%Y-%m-%d' , validators=[DataRequired(message='No dejar vacío, completar')])
    direccion = StringField('Direccion', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite la direccion de residencia"})
    ciudad = StringField('Ciudad', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite la direccion de residencia"})
    username = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite el usuario"})
    password = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite la contraseña"})
    cargo = StringField('Cargo', validators=[DataRequired(message='No dejar vacío, completar')], render_kw = {"placeholder": "Digite el cargo"})
    
