import time
import datetime
from .entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, nombre, email, password, profesor 
                    FROM users WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user=User(id=row[0], nombre=row[1], email=row[2], password=User.check_password(row[3], user.password), profesor=row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def edit(self, db, user, userId):
        try:
            userPrueba = ModelUser.get_by_email(db, user.email)
            if userPrueba == None or userPrueba.id == userId:
                cursor = db.connection.cursor()
                values = (user.nombre, user.email, generate_password_hash(user.password), userId)
                sql = "UPDATE users SET nombre = %s, email = %s, password = %s WHERE id = %s"
                cursor.execute(sql, values)
                db.connection.commit()
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_email(self, db, email):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, email, nombre, profesor FROM users WHERE email = '{}'""".format(email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(id=row[0], nombre=row[2], email=row[1], password=None, profesor=row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def create(self, db, user):
        try:
            user_email = ModelUser.get_by_email(db, user.email)
            if user_email != None:
                return None
            else:
                cursor = db.connection.cursor()
                values = (user.nombre, user.email, generate_password_hash(user.password), 0)
                sql = "INSERT INTO users (nombre, email, password, profesor) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, values)
                db.connection.commit()
                return ModelUser.login(db, user)
        except Exception as ex:
            raise Exception(ex)
        
        
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, nombre, profesor FROM users WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(id=row[0], nombre=row[2], email=row[1], password=None, profesor=row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def request_profesor(self, db, id):
        try:
            cursor = db.connection.cursor()
            tc = time.time()
            timecreate = datetime.datetime.fromtimestamp(tc).strftime('%Y-%m-%d %H:%M:%S')
            values = (id, timecreate)
            sql = "INSERT INTO profesor_request (id_user, time_create) VALUES (%s, %s)"
            cursor.execute(sql, values)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def not_exist_request(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM profesor_request WHERE id_user = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row == None:
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)