
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password%401@localhost:3306/library_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig: 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CACHE_TYPE = 'SImpleCache'


class ProductionConfig:
    pass