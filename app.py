import os
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g
from wtforms.validators import Length
from formulario import RegistroComprador, producto, Login, PerfilUsuario, formularioLogin, formularioRegistro, CambioPassword, EliminarCuenta, RegistrarOperario, ListarOperarios, lote,Comentarios
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from db import get_db, close_db

app = Flask(__name__)
app.secret_key = os.urandom(24)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def dashboard(): 
    return render_template('Home.html')

@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroComprador()
    if request.method == 'POST':
        datos = [request.form['cedula'], request.form['nombreCompleto'], request.form['sexo'], request.form['fechaNacimiento'], request.form['direccion'], request.form['ciudad'], request.form['username'], request.form['password'], "Usuario externo" ]
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
    global session
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

                return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=row,session=session['rol'])
            elif(nombre_producto == ""):

                for r in row:
                    if (id_producto in str(r['id_producto'])):
                        rowtemp.append(r)
                return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=rowtemp,session=session['rol'])
            elif(id_producto=="None"):

                for r in row:
                    if(nombre_producto in r['nombre_producto']):
                        rowtemp.append(r)
                return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=rowtemp,session=session['rol'])
            else:
                for r in row:
                    if(nombre_producto in r['nombre_producto'] and id_producto in str(r['id_producto'])):
                        rowtemp.append(r)
                return render_template('consulta_productos.html', form=form, titulo="Gestión de Productos", row=rowtemp,session=session['rol'])                

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
        return render_template('crear_productos.html', form=form, titulo="Gestión de Productos", mensaje=mensaje,session=session['rol'])


@app.route("/gestion_productos/actualizar", methods=["GET", "POST"])
def gestion_productos_actualizar():
    form = producto()
    id_producto = form.id_producto.data
    nombre_producto = form.nombre_producto.data
    unidad = form.unidad.data
    precio = form.precio.data
    promocion = form.promocion.data
    if(str(form.aplica_descuento.data) == "1"):

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
        return render_template('crear_productos.html', form=form, titulo="Gestión de Productos", mensaje=mensaje,session=session['rol'])


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
    
    return render_template('crear_productos.html', form=form, titulo="Gestión de Productos", mensaje=mensaje,session=session['rol'])

@app.route("/gestion_lote",methods=["GET", "POST"])
def gestion_lotes():
    if not session['rol']=='Usuario externo':
        form = lote()
        return render_template('crud_lotes.html', form=form, titulo="Gestión de Lotes")
    else:
        return "Usuario no Autorizado"

@app.route("/gestion_lote/crear", methods=["GET", "POST"])
def gestion_lotes_creacion():
    if not session['rol']=='Usuario externo':
        form = lote()
        id_lote = form.id_lote.data
        id_producto = form.id_producto.data
        qty_lote = form.qty_lote.data
        fecha_ingreso = form.fecha_ingreso.data

        with sqlite3.connect("db.db") as con:
            try:
                    cur = con.cursor()
                    cur.execute("INSERT INTO lotes (id_lote,id_producto,qty_lote,fecha_ingreso) VALUES (?,?,?,?)",
                                (id_lote, id_producto, qty_lote, fecha_ingreso))
                    con.commit()
                    cur.execute("SELECT qty FROM productos WHERE id_producto=?",(id_producto,))
                    row= cur.fetchone()
                    print(row)
                    row= int(row[0])+int(qty_lote)
                    cur.execute("UPDATE productos SET qty = ? WHERE id_producto = ?",[row,id_producto])
                    mensaje = "Guardado exitoso"
            except Error:
                print(Error)
                con.rollback()
                mensaje = "Ocurrió un error con el guardado del lote"
            return render_template('crear_lotes.html', form=form, titulo="Gestión de Lotes", mensaje=mensaje,session=session['rol'])
    else:
        return "Usuario no autorizado"

@app.route("/gestion_lote/consulta",methods=["GET","POST"])
def gestion_lotes_consulta():
    if not session['rol']=='Usuario externo':
        form = lote()
        id_lote = str(form.id_lote.data)
        id_producto = str(form.id_producto.data)


        with sqlite3.connect("db.db") as con:
            
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM lotes")
                row = cur.fetchall()
                rowtemp = []
                if(id_lote == 'None' and id_producto == 'None'):
                    return render_template('consulta_lotes.html', form=form, titulo="Gestión de Lotes", row=row)
                elif(id_lote == 'None'):

                    for r in row:
                        if (id_producto in str(r['id_producto'])):
                            rowtemp.append(r)
                    return render_template('consulta_lotes.html', form=form, titulo="Gestión de Lotes", row=rowtemp)
                elif(id_producto=="None"):

                    for r in row:
                        if(id_lote in r['id_lote']):
                            rowtemp.append(r)
                    return render_template('consulta_lotes.html', form=form, titulo="Gestión de Lotes", row=rowtemp)
                else:
                    for r in row:
                        if(id_lote in r['id_lote'] and id_producto in str(r['id_producto'])):
                            rowtemp.append(r)
                    return render_template('consulta_lotes.html', form=form, titulo="Gestión de Lotes", row=rowtemp)                
            except Error:
                print(Error)
                return "Ha ocurrido un error con la consulta"

    else:
        return "Usuario no autorizado"

@app.route("/gestion_lote/actualizar", methods=["GET", "POST"])
def gestion_lotes_actualizar():
    form = lote()
    id_producto = form.id_producto.data
    id_lote = form.id_lote.data
    qty_lote = form.qty_lote.data
    fecha_ingreso = str(form.fecha_ingreso.data)

    
    with sqlite3.connect("db.db") as con:
        try:
                cur = con.cursor()
                cur.execute("SELECT qty_lote FROM lotes WHERE id_lote = ?",(id_lote,))
                qty_lote_old = cur.fetchone()
                cur.execute("SELECT id_producto FROM lotes WHERE id_lote = ?",(id_lote,))
                id_producto_old = cur.fetchone()
                cur.execute("SELECT fecha_ultima_compra FROM lotes WHERE id_lote = ?",(id_lote,))
                fuc = cur.fetchone()
                if (fuc[0]=='None'):

                    if str(id_producto_old[0])==str(id_producto):
                        diff_qty=int(qty_lote_old[0])-int(qty_lote)
                        cur.execute("SELECT qty FROM productos WHERE id_producto = ?",(id_producto,))
                        qty_producto= cur.fetchone()                    
                        
                        qty_producto_nuevo = int(qty_producto[0]) - diff_qty

                        cur.execute("UPDATE productos SET qty= ? WHERE id_producto = ?",
                                [qty_producto_nuevo, id_producto])

                        cur.execute("UPDATE lotes SET qty_lote= ?, fecha_ingreso = ? WHERE id_lote = ?",
                                [qty_lote, fecha_ingreso, id_lote])

                    else:
                        print("Entra Else")
                        cur.execute("SELECT qty FROM productos WHERE id_producto = ?",(id_producto_old[0],))
                        print("Pasa primer select")
                        qty_producto= cur.fetchone()
                        qty_producto=int(qty_producto[0])-qty_lote
                        cur.execute("UPDATE productos SET qty= ? WHERE id_producto = ?",
                                [qty_producto, id_producto_old[0]])
                        print("Pasa primer Update")
                        cur.execute("UPDATE lotes SET qty_lote= ?, fecha_ingreso = ?, id_producto = ? WHERE id_lote = ?",
                                [qty_lote, fecha_ingreso, id_producto, id_lote])
                        print("Pasa Segundo Update")
                        cur.execute("SELECT qty FROM productos WHERE id_producto=?",(id_producto,))
                        row= cur.fetchone()
                        print("Pasa select")
                        row= int(row[0])+int(qty_lote)
                        cur.execute("UPDATE productos SET qty = ? WHERE id_producto = ?",[row,id_producto])
                        print("Pasa ultimo Update")
                    con.commit()
                    mensaje = "Actualización exitosa"
                else:
                    mensaje="No se puede actualizar ya que el lote ya hizo un movimiento"
                

        except Error:
            print(Error)
            con.rollback()
            mensaje = "Ocurrió un error con la actualización del producto"
        return render_template('crear_lotes.html', form=form, titulo="Gestión de Productos", mensaje=mensaje)

@app.route("/gestion_lote/eliminar", methods=["GET", "POST"])
def gestion_lotes_eliminar():
    form = lote()
    id_lote = form.id_lote.data
    
    with sqlite3.connect("db.db") as con:
        try:
                cur = con.cursor()
                cur.execute("SELECT qty_lote FROM lotes WHERE id_lote = ?",(id_lote,))
                qty_lote = cur.fetchone()
                cur.execute("SELECT id_producto FROM lotes WHERE id_lote = ?",(id_lote,))
                id_producto = cur.fetchone()
                cur.execute("SELECT fecha_ultima_compra FROM lotes WHERE id_lote = ?",(id_lote,))
                fuc = cur.fetchone()
                if (fuc[0]=='None'):

                    cur.execute("SELECT qty FROM productos WHERE id_producto = ?",(id_producto[0],))
                    qty_producto= cur.fetchone()
                    qty_producto=int(qty_producto[0])-qty_lote
                    cur.execute("UPDATE productos SET qty= ? WHERE id_producto = ?",
                            [qty_producto, id_producto[0]])
                    cur.execute("DELETE FROM lotes WHERE id_lote = ?",
                            [id_lote])
                    con.commit()
                    mensaje = "Eliminación exitosa"
                else:
                    mensaje="No se puede eliminar ya que el lote ya hizo un movimiento"
                

        except Error:
            print(Error)
            con.rollback()
            mensaje = "Ocurrió un error con la eliminació del lote"
        return render_template('crear_lotes.html', form=form, titulo="Gestión de Lotes", mensaje=mensaje)



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
                'SELECT * FROM usuarios WHERE username = ?  and Estado= "Activo"', (username, ) 
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

@app.route('/dashboard/internos/<id>/update', methods=('GET', 'POST'))
@app.route('/perfil/<id>', methods=('GET', 'POST'))
def usuario(id): 
    if 'rol' in session and 'user_id' in session:
        if session['rol'] != 'Usuario externo':
            form = PerfilUsuario()
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
                orden = "UPDATE usuarios SET cedula = ?,nombre = ?,sexo =?,fecha_nacimiento = ?,direccion = ?,ciudad = ?,username = ?, cargo = ?, rol = ? WHERE id_usuario = ? and Estado = 'Activo' "
                db = get_db()
                db.execute(orden,(datos[0], datos[1], datos[2], datos[3], datos[4],  datos[5], datos[6], datos[7], datos[8], id))
                db.commit()
                db.close()
                return redirect( url_for( 'usuario', id = id ) )  
            db.close()
            return render_template('perfilDeUsuario.html', form=form, titulo='Usuario')
        return redirect( url_for( 'usuarioLocal' ) ) 
    else:
        return redirect( url_for( 'dashboard' ) )   

@app.route('/perfil/', methods=('GET', 'POST'))
def usuarioLocal(): 
    if 'rol' in session and 'user_id' in session:
        form = PerfilUsuario()
        id = session['user_id']
        db = get_db()
        orden = "SELECT cedula, nombre,  sexo, fecha_nacimiento,  direccion,ciudad, username,cargo, rol FROM usuarios WHERE id_usuario= ? and Estado = 'Activo' "
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
            return redirect( url_for( 'usuarioLocal' ) ) 
        db.close()
        return render_template('perfilDeUsuario.html', form=form, titulo='Usuario')
    else:
        return redirect( url_for( 'dashboard' ) )  

@app.route('/perfil/password', methods=('GET', 'POST'))
def cambioContraseña( ): 
    if 'user_id' in session:
        form = CambioPassword()
        if request.method == 'POST':
            nueva = request.form['nueva'] 
            actual = request.form['actual'] 
            confirmacion = request.form['confirmacion']
            if nueva == confirmacion: 
                db = get_db()
                username = session['user_name']
                original = db.execute(
                'SELECT * FROM usuarios WHERE username = ?  ', (username, ) 
                ).fetchone()
                r = check_password_hash(original[8] , actual)
                if r:
                    db = get_db()
                    db.execute("UPDATE usuarios SET password = ? WHERE username = ? and Estado='Activo'",(generate_password_hash(nueva),username,))
                    db.commit()
                db.close()
        return render_template('cambioPassword.html', form=form, titulo='Cambio de contraseña')
    else:
        return redirect( url_for( 'dashboard' ) ) 

@app.route('/perfil/delete', methods=('GET', 'POST'))
def eliminarPerfil( ): 
    if 'user_id' in session:
        form = EliminarCuenta()
        if request.method == 'POST':
            password = request.form['password'] 
            db = get_db()
            username = session['user_name']
            original = db.execute(
            'SELECT * FROM usuarios WHERE username = ? and Estado="Activo" ', (username, ) 
            ).fetchone()
            r = check_password_hash(original[8] , password)
            if r:
                db = get_db()
                db.execute("UPDATE usuarios SET Estado = ? WHERE username = ? and Estado='Activo'",('Cerrado',username,))
                db.commit()
                db.close()
                return redirect( url_for( 'dashboard' ) )
            db.close()
        return render_template('eliminarCuenta.html', form=form, titulo='Eliminar mi cuenta')
    else:
        return redirect( url_for( 'dashboard' ) ) 

@app.route('/dashboard/internos/registro', methods=('GET', 'POST'))
def registroUsuarioInterno( ): 
    form = RegistrarOperario()
    if 'user_id' in session:
        if session['rol'] == 'Super administrador' and request.method == 'POST':
            datos = [request.form['cedula'], request.form['nombreCompleto'], request.form['sexo'], request.form['fechaNacimiento'], request.form['direccion'], request.form['ciudad'], request.form['username'], request.form['password'], request.form['cargo'], "Usuario interno" ]
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
                        orden = "INSERT INTO usuarios (cedula, nombre, sexo, fecha_nacimiento,direccion, ciudad,username, password, rol, acum_compras, num_bonos, cargo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                        db.execute(orden,(datos[0], datos[1], datos[2], datos[3], datos[4],  datos[5],datos[6], generate_password_hash(datos[7]), datos[9],0,0,datos[8]))
                        db.commit()
                        db.close()
                        return redirect( url_for( 'dashboardUsuarioInterno' ) )
                    else:
                        fallo = "Usuario ya existe en base de datos"    
                else:
                    fallo = "Cedula ya existe en base de datos"
            if fallo is not None:
                flash(fallo)
            db.close()
        return render_template('registroOperarios.html', form=form, titulo='Registrar Usuario')
    else:
        return redirect( url_for( 'dashboard' ) ) 


@app.route('/dashboard/internos', methods=('GET', 'POST'))
def dashboardUsuarioInterno( ): 
    if 'user_id' in session:
        if session['rol'] == 'Super administrador':
            form = ListarOperarios()
            db = get_db()
            usuarios = db.execute( 'SELECT id_usuario,cedula,nombre,username,cargo FROM usuarios WHERE rol = "Usuario interno" and Estado="Activo"').fetchall()
            if request.method=='POST': 
                cedula = request.form['busqueda']
                if cedula.isdigit():
                    for us in reversed(usuarios):
                        cedulaUsuario = str(us[1])
                        if not cedula in cedulaUsuario:
                            usuarios.remove(us)
            return render_template('dashboard_gestion_internos.html', usuarios = usuarios, form=form)
        return redirect( url_for( 'dashboard' ) )
    else:
        return redirect( url_for( 'dashboard' ) ) 

@app.route('/dashboard/comentarios', methods=('GET', 'POST'))
def dashboardComentarios( ): 
    if 'user_id' in session:
        if session['rol'] != 'Usuario externo':
            form = Comentarios()
            form.rangoMaximo.default = 5
            form.rangoMinimo.default = 0
            db = get_db()
            comentarios = db.execute( 'SELECT * FROM comentarios').fetchall()
            db = close_db()
            if request.method=='POST': 
                parametro = request.form['busqueda']
                filtro = request.form['filtro']
                if parametro.isdigit() and filtro=="Codigo":
                    for us in reversed(comentarios):
                        codigoProducto = str(us[2])
                        if not parametro in codigoProducto:
                            comentarios.remove(us)
                elif parametro.isdigit() and filtro=="Calificación":
                    for us in reversed(comentarios):
                        calificacion = int(us[3])
                        if int(parametro) != calificacion:
                            comentarios.remove(us)
                elif (not parametro.isdigit()) and filtro=="Calificación":
                        for us in reversed(comentarios):
                            calificacion = int(us[3])
                            max = int(request.form['rangoMaximo'])
                            min = int(request.form['rangoMinimo'])
                            if calificacion < min or calificacion > max:
                                comentarios.remove(us)
                elif parametro and filtro=="Nombre":
                    nombres = list()
                    i = 0
                    db = get_db()
                    for us in reversed(comentarios):
                        nombre = db.execute( 'SELECT nombre_producto FROM productos WHERE id_producto=?',(us[2],)).fetchall()
                        if nombre:
                            nombres.append(nombre[0][0])
                            if not parametro in nombres[i]:
                                comentarios.remove(us)
                        i += 1
            return render_template('dashboard_comentarios.html', comentarios = comentarios, form=form)
        return redirect( url_for( 'dashboard' ) )
    else:
        return redirect( url_for( 'dashboard' ) ) 

@app.route('/dashboard/comentarios/<id>/delete', methods=('GET', 'POST'))
def eliminarComentario(id): 
    if 'user_id' in session:
        if session['rol'] != 'Usuario externo':    
            if request.method == 'POST':
                db = get_db()
                db.execute("DELETE FROM comentarios WHERE id_comentario = ?",(id,))
                db.commit()
                db.close()
                return redirect( url_for( 'dashboardComentarios' ) )
            return render_template('eliminarComentario.html', id=id, titulo='Eliminar comentario')
        return redirect( url_for( 'dashboard' ) ) 
    else:
        return redirect( url_for( 'dashboard' ) ) 

@app.route('/dashboard/internos/<id>/delete', methods=('GET', 'POST'))
def eliminarPerfilOperario(id): 
    if 'user_id' in session:
        if session['rol'] == 'Super administrador':
            db = get_db()
            nombre = db.execute( 'SELECT username FROM usuarios WHERE id_usuario = ? and rol = "Usuario interno"', (id,)).fetchall()
            if len(nombre)>0:  
                nombre = nombre[0][0]
                if request.method == 'POST':
                    db.execute("UPDATE usuarios SET Estado = ? WHERE id_usuario = ? and Estado='Activo'",('Cerrado',id,))
                    db.commit()
                    db.close()
                    return redirect( url_for( 'dashboardUsuarioInterno' ) )
                return render_template('eliminarOperario.html', nombre=nombre, titulo='Eliminar cuenta')
            return redirect( url_for( 'dashboardUsuarioInterno' ) )    
        return redirect( url_for( 'dashboard' ) ) 
    else:
        return redirect( url_for( 'dashboard' ) ) 

@app.route("/producto/<id>", methods=["GET", "POST"])
def productoDetalle(id): 
    db = get_db()
    nombre = db.execute('SELECT nombre_producto, precio,unidad FROM productos WHERE id_producto = ?', (id,)).fetchall()
    listadoComentarios = db.execute('SELECT * FROM comentarios WHERE id_producto = ?',(id,)).fetchall()
    if len(nombre)>0:
        if request.method == 'POST' and 'user_id' in session:
            db.execute("INSERT into comentarios (id_usuario,id_producto,calificacion,comentario) VALUES(?,?,?,?)",(session['user_id'], id, request.form['rate'], request.form['comentario']))
            db.commit()    
        nombre = nombre[0]
        nombres = list()
        if len(listadoComentarios)>0:
            for com in listadoComentarios:
                consulta = db.execute('SELECT username FROM usuarios WHERE id_usuario = ?', (com[1],)).fetchall()
                nombres.append(consulta[0][0])
        db.close()
        return render_template('productdesc.html', product = nombre, comentario=listadoComentarios, usuarios = nombres)
    else:
        db.close()
        return redirect( url_for( 'dashboard' ) ) 
        
@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( 'dashboard' ) )   

@app.route( '/loginwtf' )
def loginwtf():
    formlogin = formularioLogin()
    formregister = formularioRegistro()
    return  render_template('loginwtf.html', formlogin= formlogin, formregister=formregister)  

if (__name__ == "__main__"):
    app.run(debug=True)
