import os


base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'it is very secret key in my application'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(base_dir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'victorsmirnov67@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'victorS77'
    ADMINS = ['victorsmirnov67@gmail.com']

    POSTS_PER_PAGE = 25