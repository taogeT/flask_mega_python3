# -*- coding: UTF-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS
from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT
import os


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler
    app.logger.setLevel(logging.INFO)
    # mail handler
    credentials = (MAIL_USERNAME, MAIL_PASSWORD) if MAIL_USERNAME or MAIL_PASSWORD else None
    mail_handler = SMTPHandler(mailhost=(MAIL_SERVER, MAIL_PORT),
                               fromaddr='no-reply@{}'.format(MAIL_SERVER),
                               toaddrs=ADMINS,
                               subject='microblog failure',
                               credentials=credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    # file handler
    file_handler = RotatingFileHandler(filename='tmp/microblog.log',
                                       maxBytes=1 * 1024 * 1024,
                                       backupCount=10,
                                       encoding='UTF-8')
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    # end
    app.logger.info('microblog startup')

from . import views, models
