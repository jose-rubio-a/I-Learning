from .entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, nombre, email, password 
                    FROM users WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user=User(id=row[0], nombre=row[1], email=row[2], password=User.check_password(row[3], user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_email(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, email, nombre FROM users WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(id=row[0], nombre=row[2], email=row[1], password=None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def create(self, db, user):
        try:
            user_email = ModelUser.get_by_email(db, user)
            if user_email != None:
                return None
            else:
                cursor = db.connection.cursor()
                values = (user.nombre, user.email, generate_password_hash(user.password))
                sql = "INSERT INTO users (nombre, email, password) VALUES (%s, %s, %s)"
                cursor.execute(sql, values)
                db.connection.commit()
                return ModelUser.login(db, user)
        except Exception as ex:
            raise Exception(ex)
        
        
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, nombre FROM users WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(id=row[0], nombre=row[2], email=row[1], password=None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)