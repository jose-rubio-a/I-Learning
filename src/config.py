class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Alvarez&26'
    MYSQL_DB = 'flask_login'

config = {
    'development': DevelopmentConfig
}