import boto3
from textblob import TextBlob
from flask import Flask,render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from forms import RegistroForm, EditarForm, CrearCursoForm, EditarCursoForm, CrearReviewForm, CrearActividadForm

from config import config

#Models
from models.ModelUser import ModelUser
from models.ModelCurso import ModelCurso
from models.ModelReview import ModelReview
from models.ModelActividad import ModelActividad

#Entities
from models.entities.User import User
from models.entities.Curso import Curso
from models.entities.Review import Review
from models.entities.Actividad import Actividad


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

@app.route('/cursos/<int:curso_id>')
def show_curso(curso_id):
    curso = ModelCurso.get_by_id(db, curso_id)
    if curso != None:
        user = ModelUser.get_by_id(db, curso.user_id)
        reviews = ModelReview.get_table(db, curso_id=curso_id)
        actividades = ModelActividad.get_actividades(db, curso_id=curso_id)
        return render_template('show-curso.html', curso=curso, user=user, reviews=reviews, actividades=actividades)
    else:
        return redirect(url_for('cursos'))
    
@app.route('/curso/<int:curso_id>/actividad/<int:actividad_id>')
def show_actividad(actividad_id, curso_id):
    actividad = ModelActividad.get_actividad_id(db, actividad_id=actividad_id)
    if actividad != None:
        curso = ModelCurso.get_by_id(db, curso_id)
        user = ModelUser.get_by_id(db, curso.user_id)
        return render_template('show-actividad.html', curso=curso, actividad=actividad, user=user)
    else:
        return redirect(url_for('show_curso', curso_id=curso_id))

@app.route('/cursos', methods=['POST', 'GET'])
def cursos():
    row = []
    if request.method == 'POST':
        nombre = request.form['busqueda']
        row = ModelCurso.get_by_name(db, nombre)
    return render_template('cursos.html', cursos=row)   

@app.route('/profesores')
def profesores():
    return render_template('profesores.html')

@app.route('/perfil/<int:user_id>')
@login_required
def perfil(user_id):
    row = ModelCurso.get_by_user(db, user_id)
    return render_template('perfil.html', cursos=row)

@app.route('/crear_curso/', defaults={'user_id': None})
@app.route('/crear_curso/<int:user_id>', methods=['POST'])
@login_required
def crear_curso(user_id):
    form = CrearCursoForm() 
    if form.validate_on_submit():
        curso = Curso(id=0, user_id=user_id, nombre=form.nombreCurso.data, informacion=form.informacionCurso.data, timecreate=None, timeupdate=None)
        ModelCurso.create(db, curso)
        return redirect(url_for('cursos'))
    else:
        flash(form.errors)
        return render_template('crear-curso.html', form=form)

@app.route('/crear_actividad/<int:curso_id>', methods=['POST', 'GET'])
@login_required
def crear_actividad(curso_id):
    form = CrearActividadForm()
    if form.validate_on_submit():
        actividad = Actividad(id=0, curso_id=curso_id, nombre=form.nombreActividad.data, texto=form.textoActividad.data, timecreate=None, timeupdate=None)
        ModelActividad.createActividad(db, actividad=actividad)
        return redirect(url_for('show_curso', curso_id=curso_id))
    else:
        flash(form.errors)
        return render_template('crear-actividad.html', form=form, curso_id=curso_id)
    
@app.route('/feedback/<int:curso_id>', methods=['POST', 'GET'])
def feedback(curso_id):
    aws_mag_con=boto3.session.Session(profile_name="demo2")
    client=aws_mag_con.client(service_name='comprehend',  region_name="us-east-1")
    form = CrearReviewForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data
        informacion = form.informacion.data
        sentimiento = None 
        # Realiza el análisis de sentimiento utilizando Amazon Comprehend
        # Crea una instancia del modelo Review con el sentimiento
       
        response = client.detect_sentiment(Text=informacion, LanguageCode='es')
        sentimiento = response['Sentiment']

        #Realiza la deteccion de lenguaje
        response2 = client.detect_dominant_language(Text=informacion)
        #dominant_language nos da el código del lenguaje dominante, ej "es=español", "en=english",
        dominant_language = response2["Languages"][0]["LanguageCode"]
        #idioma nos da el análisis completo del idioma del texto con el score exacto
        idioma = response2["Languages"][0]["Score"]
        print(response2)
        print(f"Dominant Language: {dominant_language}")
        print(f"Confidence: {idioma}")

        review = Review(nombre=nombre, correo=correo, informacion=informacion, sentimiento=sentimiento,idioma=dominant_language, curso_id=curso_id)
        # Guarda la revisión en la base de datos
        ModelReview.createRev(db, review)

        
        

        flash('Opinión creada exitosamente.')
        return redirect(url_for('index'))

    return render_template('feedback.html', form=form, curso_id=curso_id)
    

    
    
@app.route('/cursos/<int:curso_id>/edit', methods=['POST', 'GET'])
@login_required
def editar_curso(curso_id):
    form = EditarCursoForm()
    curso = ModelCurso.get_by_id(db, curso_id)
    if form.validate_on_submit():
        cursoEdit = Curso(id=curso_id, user_id=0, nombre=form.nombreCurso.data, informacion=form.informacionCurso.data, timecreate=None, timeupdate=None)
        curso = ModelCurso.editar_curso(db, cursoEdit)
        return redirect(url_for('show_curso', curso_id=curso_id))
    else:
        flash(form.errors)
        return render_template('edit-curso.html', form=form, curso=curso)
    
@app.route('/cursos/<int:curso_id>/delete', methods=['POST'])
@login_required
def eliminar_curso(curso_id):
    ModelCurso.eliminar_curso(db, curso_id)
    return redirect(url_for('cursos'))


@app.route('/editar_perfil/', defaults={'user_id': None})
@app.route('/editar_perfil/<int:user_id>', methods=['POST'])
@login_required
def edit_perfil(user_id):
    form = EditarForm()
    if form.validate_on_submit():
        user = User(id=0, nombre=form.nombre.data, password=form.password.data, email=form.email.data)
        logged_user = ModelUser.edit(db, user, user_id)
        if logged_user != None:
            return redirect(url_for('perfil', user_id=user_id))
        else:
            errors = {'email': ['Correo Existente']}
            flash(errors)
            return redirect(url_for('edit_perfil'))
    else:
        flash(form.errors)
        return render_template('editar-perfil.html', form=form)

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
                errors = {'passwordLog': ['Contraseña Invalida']}
                flash(errors)
                return redirect(url_for('sesion'))
        else:
            errors = {'emailLog': ['Usuario no encontrado']}
            flash(errors)
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