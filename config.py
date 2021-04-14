import secrets
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = secrets.token_urlsafe(16)
    SECURITY_PASSWORD_SALT = secrets.token_urlsafe(16)
    # database
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # mail settings
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # gmail authentication
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    # main accounts
    MAIL_DEFAULT_SENDER = ""
    #Petfinder
    KEY =""
    SECRET =""

class ProductionConfig(Config):
    # Database
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI ="sqlite:///./dbs/production.sqlite3"
    SQLALCHEMY_ECHO = False
    # Upload paths
    POST_UPLOADS = "./flask_app/static/img/posts/"
    PET_UPLOADS = "./flask_app/static/img/pets/"
    PROFILE_UPLOADS = "./flask_app/static/img/profiles/"

class DevelopmentConfig(Config):
    DEBUG = True

    POST_UPLOADS = "./flask_app/static/img/posts/"
    PET_UPLOADS = "./flask_app/static/img/pets/"
    PROFILE_UPLOADS = "./flask_app/static/img/profiles/"

    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI ="sqlite:///./dbs/development.sqlite3"
    SQLALCHEMY_ECHO = False
    EXTEND_EXISTING = True


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "test-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False
