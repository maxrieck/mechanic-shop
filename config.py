
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password%401@localhost:3306/library_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig:
    pass

class ProductionConfig:
    pass