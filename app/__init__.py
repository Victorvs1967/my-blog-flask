import os
import logging
import psycopg2
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_babel import Babel, _, lazy_gettext as _l
from flask_moment import Moment
from elasticsearch import Elasticsearch
from redis import Redis
import rq
from flask_admin import Admin


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
bootstrap = Bootstrap()
babel = Babel()
moment = Moment()
admin = Admin()
admin.name = 'My Blog: Admin'


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    moment.init_app(app)
    admin.init_app(app)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('server-tasks', connection=app.redis)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=f'no-reply@{app.config["MAIL_SERVER"]}',
                toaddrs=app.config['ADMINS'],
                subject=_('My Blog Failure'),
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/myblog.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info(_('My blog startup'))

    return app

from app import models