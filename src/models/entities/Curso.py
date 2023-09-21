import datetime

class Curso():

    def __init__(self, id, user_id, nombre, informacion) -> None:
        self.id = id
        self.user_id = user_id
        self.nombre = nombre
        self.informacion = informacion
        self.create = datetime.datetime.now()
        self.update = datetime.datetime.now()