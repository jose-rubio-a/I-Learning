from .entities.Curso import Curso
import time
import datetime

class ModelCurso():

    @classmethod
    def create(self, db, curso):
        try:
            cursor = db.connection.cursor()
            tc = time.time()
            timecreate = datetime.datetime.fromtimestamp(tc).strftime('%Y-%m-%d %H:%M:%S')
            values = (curso.user_id, curso.nombre, curso.informacion, timecreate, timecreate)
            sql = "INSERT INTO cursos (user_id, nombre, informacion, time_create, time_update) VALUES (%s, %s, %s, %s, %s)"
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