from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, nombre, password, email, profesor) -> None:
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.profesor = profesor

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)