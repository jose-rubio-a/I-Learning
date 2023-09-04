from werkzeug.security import check_password_hash, generate_password_hash

class User():

    def __init__(self, id, nombre, password, email) -> None:
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)