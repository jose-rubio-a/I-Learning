from flask import Flask,render_template, url_for

app = Flask(__name__)

#Rutas de la aplicacion
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sesion')
def sesion():
    return render_template('sesion.html')

if __name__ == '__main__':
    app.run(debug=True, port=4000)