from .entities.Curso import Curso
import datetime

class ModelCurso():

    @classmethod
    def create(self, db, curso):
        try:
            cursor = db.connection.cursor()
            values = (curso.user_id, curso.nombre, curso.informacion)
            sql = "INSERT INTO cursos (user_id, nombre, informacion) VALUES (%s, %s, %s)"
            cursor.execute(sql, values)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_name(self, db, nombre):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT nombre, informacion FROM cursos WHERE nombre LIKE '%{}%'""".format(nombre)
            cursor.execute(sql)
            row = cursor.fetchall()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)