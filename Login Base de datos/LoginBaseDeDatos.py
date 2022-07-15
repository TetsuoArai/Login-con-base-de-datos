from flask import Flask, render_template, request, flash
import sqlite3
import time

app = Flask(__name__)

app.config['SECRET_KEY']= 'Arai'

db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/sesion', methods=['POST'])
def sesion():
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']

    date_user = cursor.execute(f"SELECT contraseña FROM registros WHERE usuario='{usuario}'")
    date_database = date_user.fetchall()
    
    valor = False
    resultado = 'False'
    for x in date_database:
        for y in x:
            if y == contraseña:
                valor = True
                resultado = 'True'
                if resultado == 'True':
                    flash('Iniciaste sesion correctamente!', 'success')
        
        if valor == True:
            break
    if valor == False:
        if resultado == 'False':
            flash('Su contraseña o su usuario es incorrecto', 'danger')
    
    return render_template('base.html')

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')

@app.route('/user', methods=['POST'])
def user():
    nombre = request.form['nombre']
    usuario = request.form['usuario']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    
    datos = nombre, usuario, correo, contraseña

    base_usuario = cursor.execute('SELECT usuario FROM registros')
    date_usuario = base_usuario.fetchall()

    valor = False
    resultado = 'True'
    for x in date_usuario:
        for y in x:
            if y == usuario:
                valor = True
                resultado = 'False'
                if resultado == 'False':
                    flash('Error, este usuario ya existe', 'danger')
    
        if valor == True:
            break
    if valor == False:
        if resultado == 'True':
            flash('Se ha registrado correctamente', 'success')
            cursor.execute('INSERT into registros(nombre, usuario, correo, contraseña) VALUES(?, ?, ?, ?)', datos)
            db.commit()
            time.sleep(2)
    return render_template('registrarse.html')

if __name__== '__main__':
    app.run(debug=True, port=1500)