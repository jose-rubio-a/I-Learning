from .entities.Review import Review
import time
import datetime

class ModelReview():

    @classmethod
    def createRev(self, db, review):
        try:
            cursor = db.connection.cursor()
            values = (review.nombre, review.correo, review.informacion, review.sentimiento,review.idioma, review.curso_id)
            sql = "INSERT INTO reviews (nombre, correo, informacion, sentimiento,idioma, curso_id) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, values)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_table(self, db, curso_id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT nombre, correo, informacion, sentimiento, idioma FROM reviews WHERE curso_id = {}""".format(curso_id)
            cursor.execute(sql)
            row = cursor.fetchall()
            if row != None:
                return row
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_sentimientos(self, db, curso_id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT * FROM reviews WHERE curso_id = {}""".format(curso_id)
            total_count = cursor.execute(sql)

            if total_count > 0:
                sql = "SELECT * FROM reviews WHERE curso_id = {} AND sentimiento = 'POSITIVE'".format(curso_id)
                positive_count = cursor.execute(sql)
                sql = "SELECT * FROM reviews WHERE curso_id = {} AND sentimiento = 'NEGATIVE'".format(curso_id)
                negative_count = cursor.execute(sql)
                return [round(positive_count/total_count, 2), round(negative_count/total_count, 2), round((total_count-positive_count-negative_count)/total_count, 2)]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
