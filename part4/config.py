import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {  
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}