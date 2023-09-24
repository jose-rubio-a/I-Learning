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
    def editar_curso(self, db, curso):
        try:
            cursoUpdate = ModelCurso.get_by_id(db, curso.id)
            if cursoUpdate:
                cursor = db.connection.cursor()
                tu = time.time()
                timeupdate = datetime.datetime.fromtimestamp(tu).strftime('%Y-%m-%d %H:%M:%S')
                values = (curso.nombre, curso.informacion, timeupdate, curso.id)
                sql = "UPDATE cursos SET nombre = %s, informacion = %s, time_update = %s WHERE id = %s"
                cursor.execute(sql, values)
                db.connection.commit()
                return curso
            else: 
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def eliminar_curso(self, db, curso_id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM cursos WHERE id = {}".format(curso_id)
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_name(self, db, nombre):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT nombre, informacion, time_create, time_update, id FROM cursos WHERE nombre LIKE '%{}%'""".format(nombre)
            cursor.execute(sql)
            row = cursor.fetchall()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, user_id, nombre, informacion, time_create, time_update FROM cursos WHERE id = {}""".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                curso=Curso(id=row[0], user_id=row[1], nombre=row[2], informacion=row[3], timecreate=row[4], timeupdate=row[5])
                return curso
            else:
                return None
        except Exception as ex:
            raise Exception(ex)