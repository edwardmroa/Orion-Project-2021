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
    nombre_producto = str(form.nombre_producto.data)
    id_producto = str(form.id_producto.data)
    try:
        with sqlite3.connect("db.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM productos")
            row = cur.fetchall()
            rowtemp = []

            if(nombre_producto == '' and id_producto == 'None'):

                return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=row)
            elif(nombre_producto == ""):

                for r in row:
                    if (id_producto in str(r['id_producto'])):
                        rowtemp.append(r)
                return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=rowtemp)
            elif(id_producto=="None"):

                for r in row:
                    if(nombre_producto in r['nombre_producto']):
                        rowtemp.append(r)
                return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=rowtemp)
            else:
                for r in row:
                    if(nombre_producto in r['nombre_producto'] and id_producto in str(r['id_producto'])):
                        print("Pasa if interno nombre y ID llenos")
                        rowtemp.append(r)
                return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=rowtemp)                

    except Error:
        print(Error)
        return "Ocurrió un error, vuelva a intentar"   


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
    if(form.aplica_descuento.data == "1"):
        aplica_descuento = True
    else:
        aplica_descuento = False
    acum_descontado = 0
    categoria = "Baja"
    baja = "False"

    with sqlite3.connect("db.db") as con:
        try:
                cur = con.cursor()
                cur.execute("INSERT INTO productos (id_producto,nombre_producto,qty,unidad,precio,promocion,num_ventas,total_ventas,calificacion,aplica_descuento,acum_descontado,categoria,baja) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (id_producto, nombre_producto, qty, unidad, precio, promocion, num_ventas, total_ventas, calificacion, aplica_descuento, acum_descontado, categoria, baja))
                con.commit()
                mensaje = "Guardado exitoso"

        except Error:
            print(Error)
            con.rollback()
            mensaje = "Ocurrió un error con el guardado del producto"
        return render_template('crear_productos.html', form=form, titulo="Gestión de Productos", mensaje=mensaje)


@app.route("/gestion_productos/actualizar", methods=["GET", "POST"])
def gestion_productos_actualizar():
    form = producto()
    id_producto = form.id_producto.data
    nombre_producto = form.nombre_producto.data
    unidad = form.unidad.data
    precio = form.precio.data
    promocion = form.promocion.data
    if(str(form.aplica_descuento.data) == "1"):
        print("pasa if")
        aplica_descuento = True
    else:
        aplica_descuento = False

    with sqlite3.connect("db.db") as con:
        try:
                cur = con.cursor()
                cur.execute("UPDATE productos SET nombre_producto = ?, unidad = ?, precio = ?, promocion = ?, aplica_descuento= ? WHERE id_producto = ?",
                            [nombre_producto, unidad, precio, promocion, aplica_descuento, id_producto])
                con.commit()
                mensaje = "Actualización exitosa"

        except Error:
            print(Error)
            con.rollback()
            mensaje = "Ocurrió un error con la actualización del producto"
        return render_template('crear_productos.html', form=form, titulo="Gestión de Productos", mensaje=mensaje)


@app.route("/gestion_productos/eliminar", methods=["GET", "POST"])
def gestion_productos_eliminar():
    form = producto()
    id_producto = form.id_producto.data

    with sqlite3.connect("db.db") as con:
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM productos WHERE id_producto=?", [id_producto])
            if (con.total_changes > 0):
                mensaje = "Producto borrado"
            else:
                mensaje = "Producto no encontrado"
                
        except Error:
            print(Error)
            mensaje = "Error"
    
    return render_template('crear_productos.html', form=form, titulo="Gestión de Productos", mensaje=mensaje)

if (__name__ == "__main__"):
    app.run(debug=True)
