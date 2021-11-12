import os
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g
from formulario import RegistroComprador, producto
app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def dashboard():

    return "Home"


@app.route("/registroComprador", methods=["GET", "POST"])
def registroComprador():
    form = RegistroComprador()
    return render_template('registroComprador.html', form=form, titulo='Registrar Usuario')


@app.route("/gestion_productos", methods=["GET", "POST"])
def gestion_productos():
    form = producto()
    return render_template('crud_productos.html', form=form, titulo="Gestión de Productos")


@app.route("/gestion_productos/consulta", methods=["GET", "POST"])
def gestion_productos_consulta():
    form = producto()
    nombre_producto=str(form.nombre_producto.data)
    id_producto=str(form.id_producto.data)
    try:
        with sqlite3.connect("db.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM productos")
            row = cur.fetchall()            
    except Error:
        print(Error)
        return "Ocurrió un error, vuelva a intentar"

    rowtemp=[]

    if(nombre_producto=='' and id_producto==''):
        return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=row)
    elif(nombre_producto == ""):
        for r in row:
            if (id_producto in str(r['id_producto'])):
                rowtemp.append(r)
        return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=rowtemp)
    else:
        for r in row:
            if(nombre_producto in r['nombre_producto']):
                rowtemp.append(r)
        return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=rowtemp)
    


@app.route("/gestion_productos/crear", methods=["GET", "POST"])
def gestion_productos_creacion():
    form = producto()
    id_producto = form.id_producto.data
    nombre_producto = form.nombre_producto.data
    qty = 0
    unidad = form.unidad.data
    precio = form.precio.data
    promocion = form.promocion.data
    num_ventas = 0
    total_ventas = 0
    calificacion = 0
    if(form.aplica_descuento.data=="Si"):
        aplica_descuento = True
    else:
        aplica_descuento = False 
    acum_descontado = 0
    categoria = "Baja"
    baja="False"

    with sqlite3.connect("db.db") as con:
        try:
                cur = con.cursor()
                cur.execute("INSERT INTO productos (id_producto,nombre_producto,qty,unidad,precio,promocion,num_ventas,total_ventas,calificacion,aplica_descuento,acum_descontado,categoria,baja) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (id_producto, nombre_producto, qty, unidad, precio, promocion,num_ventas,total_ventas,calificacion,aplica_descuento,acum_descontado,categoria,baja))
                con.commit()
                mensaje="Guardado exitoso"
                
        except Error:
            print(Error)
            con.rollback()
            mensaje="Ocurrió un error con el guardado del producto"
        return render_template('crear_productos.html', form=form, titulo="Gestión de Productos", mensaje=mensaje)

@app.route("/gestion_productos/actualizar")
def gestion_productos_actualizar():
    form=producto()
    


if (__name__ == "__main__"):
    app.run(debug=True)
