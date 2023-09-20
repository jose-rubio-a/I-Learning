from flask import Flask,render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from forms import RegistroForm

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

@app.route('/edit')
@login_required
def edit_form():
    return render_template('editar-perfil.html')

@app.route('/editar_perfil', methods=['POST'])
@login_required
def edit_perfil():
    pass

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sesion'))

def status_401(error):
    return redirect(url_for('sesion'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>", 404

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    if request.method=="POST":
        user=User(id=0, nombre="", email=request.form['emailLog'], password=request.form['passwordLog'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('index'))
            else:
                flash("Contraseña Invalida")
                return redirect(url_for('sesion'))
        else:
            flash("Usuario no encontrado")
            return redirect(url_for('sesion'))
    else:
        return render_template('sesion.html')
    
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    form = RegistroForm()
    if form.validate_on_submit():
        user = User(id=0, nombre=form.nombreRegistro.data, password=form.passwordRegistro.data, email=form.emailRegistro.data)
        logged_user = ModelUser.create(db,user)
        if logged_user != None:
            login_user(logged_user)
            return redirect(url_for('index'))
        else:
            errors = {'emailRegistro': ['Correo Existente']}
            flash(errors)
            return redirect(url_for('sesion'))
    else:
        flash(form.errors)
        return redirect(url_for('sesion'))

@app.route('/sesion')
def sesion():
    form = RegistroForm()
    return render_template('sesion.html', form=form)

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port=4000)