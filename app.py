import os
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g
from formulario import RegistroComprador, producto, Login, PerfilUsuario
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from db import get_db, close_db

app = Flask(__name__)
app.secret_key = os.urandom(24)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def dashboard():

    return "Home"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroComprador()
    if request.method == 'POST':
        datos = [request.form['cedula'], request.form['nombreCompleto'], request.form['sexo'], request.form['fechaNacimiento'], request.form['direccion'], request.form['ciudad'], request.form['username'], request.form['password'], "Comprador" ]
        cedula = datos[0]
        fechaDeNacimiento = datos[3]
        fechaDeNacimiento = fechaDeNacimiento.split("-")
        celular = datos[5]   
        #fallo = validarDatosDeUsuario(datos[7],correo,fechaDeNacimiento,celular,identificacion)
        fallo = None
        db= get_db()
        if  fallo == None:
            orden = "SELECT id_usuario FROM usuarios WHERE cedula= ?"
            if db.execute(orden,(datos[0],)).fetchone()  == None:
                orden = "SELECT id_usuario FROM usuarios WHERE username= ?"
                if db.execute(orden,(datos[6],)).fetchone() == None:
                    orden = "INSERT INTO usuarios (cedula, nombre, sexo, fecha_nacimiento,direccion, ciudad,username, password, rol, acum_compras, num_bonos) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
                    db.execute(orden,(datos[0], datos[1], datos[2], datos[3], datos[4],  datos[5],datos[6], generate_password_hash(datos[7]), datos[8],0,0))
                    db.commit()
                    db.close()
                    return redirect( url_for( 'registro' ) )
                else:
                    fallo = "Usuario ya existe en base de datos"    
            else:
               fallo = "Cedula ya existe en base de datos"
        if fallo is not None:
            flash(fallo)
        db.close()
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
        return "Ocurrió un error, vuelva a intentar"

@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    try:
        if request.method == 'POST':
            db = get_db()
            error = None
            username = request.form['username']
            password = request.form['password']
            error = None
            # if not username:
            #     error = 'Debes ingresar el usuario'
            #     flash( error )

            # #if not validacion.isUsernameValid(username):
            #     error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
            #     flash(error)

            # #if not password:
            #     error = 'Contraseña requerida'
            #     flash( error )
            
            print(password)
            print(generate_password_hash(password))
            user = db.execute(
                'SELECT * FROM usuarios WHERE username = ?  ', (username, ) 
            ).fetchone()
            close_db()
            if user is None:
                error = 'Usuario o contraseña inválidos'
                flash(error)

            else:                           
                passwordDataBase= user[8]
                resultado=check_password_hash(passwordDataBase,password)

                if(not resultado):
                    error = 'Usuario o contraseña inválidos'
                    flash(error)
                else:
                    session.clear()
                    session['user_id'] = user[0]
                    session['user_name'] = user[7]
                    session['rol'] = user[10]
                    return redirect( url_for( 'dashboard' ) ) 
                    
        return render_template('login.html', form=form, titulo='Inicio de sesión')
    except:
        return render_template('login.html', form=form, titulo='Inicio de sesión')


@app.route('/perfil', methods=('GET', 'POST'))
def usuario( ): 
    form = PerfilUsuario()
    if session['user_id'] !=None:
        id = session['user_id']
        db = get_db()
        orden = "SELECT cedula, nombre,  sexo, fecha_nacimiento,  direccion,ciudad, username,cargo, rol FROM usuarios WHERE id_usuario= ?"
        data = db.execute(orden, (id,)).fetchone()
        form.cedula.default = data[0]
        form.nombreCompleto.default = data[1]
        form.sexo.default = data[2]
        form.fechaNacimiento.default =  datetime.strptime(data[3],'%Y-%m-%d')
        form.direccion.default = data[4]
        form.ciudad.default = data[5]
        form.username.default = data[6]
        form.cargo.default = data[7]
        form.rol.default = data[8]
        form.process()
        if request.method == 'POST':
            datos = [request.form['cedula'], request.form['nombreCompleto'], request.form['sexo'], request.form['fechaNacimiento'], request.form['direccion'], request.form['ciudad'], request.form['username'], request.form['cargo'], request.form['rol']  ]
            #if validarDatosDeUsuario("NombreValido",correo,fechaDeNacimiento,celular,identificacion) ==  None:
            orden = "UPDATE usuarios SET cedula = ?,nombre = ?,sexo =?,fecha_nacimiento = ?,direccion = ?,ciudad = ?,username = ?, cargo = ?, rol = ? WHERE id_usuario = ?"
            db = get_db()
            db.execute(orden,(datos[0], datos[1], datos[2], datos[3], datos[4],  datos[5], datos[6], datos[7], datos[8], id))
            db.commit()
            db.close()
        db.close()
    return render_template('perfilDeUsuario.html', form=form, titulo='Usuario')
  
@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( 'dashboard' ) )   

if (__name__ == "__main__"):
    app.run(debug=True)
