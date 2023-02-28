from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='' 
app.config['MYSQL_DATABASE_DB']='empleados'
app.config['SECRET_KEY'] = "nacho123"

UPLOADS = os.path.join('uploads/')
app.config['UPLOADS'] = UPLOADS 

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/fotodeusuario/<path:nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('UPLOADS'), nombreFoto)

@app.route('/')
def index():
    sql = "SELECT * FROM empleados;"    
    cursor.execute(sql)
    empleados = cursor.fetchall()
    conn.commit()
    return render_template('empleados/index.html', empleados = empleados)

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    if _nombre == '' or _correo =='':
        flash('El nombre y el correo son obligatorios')
        return redirect('/create')

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    sql = "SELECT foto FROM empleados WHERE id=(%s)"
    datos = [id]
    cursor.execute(sql, datos)

    nombreFoto = cursor.fetchone()[0]
    try:
        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
    except:
        pass

    sql = "DELETE FROM empleados WHERE id=(%s)"
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/') 

@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM empleados WHERE id=(%s)"
    datos = [id]
    
    cursor.execute(sql, datos)
    empleado = cursor.fetchone()
    print(empleado)
    conn.commit()
    return render_template('empleados/edit.html', empleado=empleado)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

        sql = "SELECT foto FROM empleados WHERE ID=(%s)"
        datos = [id]
        cursor.execute(sql, datos)        
        conn.commit()

        nombreFoto = cursor.fetchone()[0]
        borrarEstaFotoDeLaDB = os.path.join(app.config['UPLOADS'], nombreFoto)
        print(borrarEstaFotoDeLaDB)
        
        try:
            os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
        except:
            pass

        sql = f'UPDATE empleados SET foto="{nuevoNombreFoto}" WHERE id="{id}";'
        cursor.execute(sql)
        conn.commit()
          
     
    sql = f'UPDATE empleados SET nombre="{_nombre}", correo="{_correo}" WHERE id="{id}"'
    
    cursor.execute(sql)
    conn.commit()
    
    return redirect('/')

 

if __name__ == '__main__':
    app.run(debug=True)