from .entities.Actividad import Actividad
import time
import datetime

class ModelActividad():

    @classmethod
    def createActividad(self, db, actividad):
        try:
            cursor = db.connection.cursor()
            tc = time.time()
            timecreate = datetime.datetime.fromtimestamp(tc).strftime('%Y-%m-%d %H:%M:%S')
            values = (actividad.curso_id, actividad.nombre, actividad.texto, timecreate, timecreate)
            sql = "INSERT INTO actividades (id_curso, nombre, texto, time_create, time_update) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, values)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_actividades(self, db, curso_id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, nombre FROM actividades WHERE id_curso = {}""".format(curso_id)
            cursor.execute(sql)
            row = cursor.fetchall()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def editar_actividad(self, db, actividad):
        try:
            actividadUpdate = ModelActividad.get_actividad_id(db, actividad.id)
            if actividadUpdate:
                cursor = db.connection.cursor()
                tu = time.time()
                timeupdate = datetime.datetime.fromtimestamp(tu).strftime('%Y-%m-%d %H:%M:%S')
                values = (actividad.nombre, actividad.texto, timeupdate, actividad.id)
                sql = "UPDATE actividades SET nombre = %s, texto = %s, time_update = %s WHERE id = %s"
                cursor.execute(sql, values)
                db.connection.commit()
                return actividad
            else: 
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def eliminar_actividad(self, db, actividad_id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM actividades WHERE id = {}".format(actividad_id)
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_actividad_id(self, db, actividad_id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_curso, nombre, texto, time_create, time_update FROM actividades WHERE id = {}""".format(actividad_id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                actividad=Actividad(id=actividad_id, curso_id=row[0], nombre=row[1], texto=row[2], timecreate=row[3], timeupdate=row[4])
                return actividad
            else:
                return None
        except Exception as ex:
            raise Exception(ex)