import os
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g
from formulario import RegistroComprador 
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


if (__name__=="__main__"):
    app.run(debug=True)