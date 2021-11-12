import os,sqlite3
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
    return render_template('crud_productos.html',form=form,titulo="Gestión de Productos")

@app.route("/gestion_productos/consulta", methods=["GET", "POST"])
def gestion_productos_consulta():
    form = producto()
    tipo="consulta"
    try:
        with sqlite3.connect("db.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM productos")
            row = cur.fetchall()
            return render_template('consulta_productos.html',form=form,titulo="Gestión de Productos",tipo=tipo,row=row) 
    except Error:
        print(Error)
        return "Ocurrió un error, vuelva a intentar"
    
    

if (__name__=="__main__"):
    app.run(debug=True)