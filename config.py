import os
from dotenv import load_dotenv


base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'it is very secret key in my application'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(base_dir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMINS = ['victorsmirnov67@gmail.com']

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS' or True)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL' or True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME' or 'victorsmirnov67@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD' or 'victorS77')
    MAIL_DEFAULT_SENDER = ADMINS[0]

    POSTS_PER_PAGE = 7
    LANGUAGES = ['en', 'ru']

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
