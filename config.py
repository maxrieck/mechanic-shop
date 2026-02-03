import os
from dotenv import load_dotenv


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{os.environ.get('DB_PASSWORD')}@localhost:3306/library_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig: 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CACHE_TYPE = 'SImpleCache'


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = 'SimpleCache'