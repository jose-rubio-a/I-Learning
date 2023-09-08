from .entities.User import User

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