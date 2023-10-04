import datetime

class Review():

    def __init__(self, nombre, correo, informacion, sentimiento, idioma, curso_id) -> None:
        self.correo = correo
        self.nombre = nombre
        self.informacion = informacion
        self.sentimiento = sentimiento
        self.idioma = idioma
        self.curso_id = curso_id