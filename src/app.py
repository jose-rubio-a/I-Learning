from flask import Flask,render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

#Models
from models.ModelUser import ModelUser

#Entities
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id);

#Rutas de la aplicacion
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/profesores')
def profesores():
    return render_template('profesores.html')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sesion'))

def status_401(error):
    return redirect(url_for('sesion'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>", 404

@app.route('/sesion', methods=['GET', 'POST'])
def sesion():
    if request.method=="POST":
        user=User(id=0, nombre="", email=request.form['emailLog'], password=request.form['passwordLog'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
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
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port=4000)