class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "don't tell anyone"

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS = "/home/username/app/app/static/images/uploads" 

    PET_MODEL= "./image_classifier/pet_model/"

    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI ="mysql://user:''@localhost:3306/competdium" 

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"

    POST_UPLOADS = "./competdium_app/static/img/posts/"
    PET_UPLOADS = "./competdium_app/static/img/pets/"
    PROFILE_IMAGES_UPLOADS = "/static/img/users/"

    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI ="sqlite:///./db.sqlite3"
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False