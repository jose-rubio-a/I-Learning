from flask import Flask,render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL

from config import config

#Models
from models.ModelUser import ModelUser

#Entities
from models.entities.User import User

app = Flask(__name__)

db = MySQL(app)

#Rutas de la aplicacion
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sesion', methods=['GET', 'POST'])
def sesion():
    if request.method=="POST":
        user=User(id=0, nombre="", email=request.form['emailLog'], password=request.form['passwordLog'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('index'))
            else:
                flash("Invalid Password...")
                return render_template('sesion.html')
        else:
            flash("User not foud...")
            return render_template('sesion.html')
    else:
        return render_template('sesion.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=4000)