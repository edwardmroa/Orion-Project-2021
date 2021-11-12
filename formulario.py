from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,  IntegerField, SelectField, DateField, FloatField
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