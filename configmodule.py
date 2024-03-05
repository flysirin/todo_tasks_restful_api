from config import DB_LOGIN, DB_PASS, DB_PORT, DB_HOST, DB_NAME


class Config(object):
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DB_TEST_NAME = "test_mysql_db"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}"
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
