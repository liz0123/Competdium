class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "don't tell anyone"

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI ="mysql://user:''@localhost:3306/competdium" 

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"

    POST_UPLOADS = "C:/Users/isabe/Projects/Competdium/app/static/img/posts/"
    POST_FOLDER = "../static/img/posts/"
    PROFILE_IMAGES_UPLOADS = "/static/img/users/"

    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI ="sqlite:///./dbs.sqlite3"
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False