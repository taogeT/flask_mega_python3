# -*- coding: UTF-8 -*-

from flask import Flask
from flask.json import JSONEncoder
from speaklater import is_lazy_string
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.mail import Mail
from flask.ext.babel import Babel, lazy_gettext
from config import basedir, ADMINS
from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT
from .momentjs import momentjs
import os


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = lazy_gettext('Please log in to access this page.')
oid = OpenID(app, os.path.join(basedir, 'tmp'))
mail = Mail(app)
babel = Babel(app)

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

app.jinja_env.globals['momentjs'] = momentjs


class CustomJSONEncoder(JSONEncoder):
    """This class adds support for lazy translation texts to Flask's
    JSON encoder. This is necessary when flashing translated texts."""
    def default(self, obj):
        return str(obj) if is_lazy_string(obj) else super(CustomJSONEncoder, self).default(obj)

app.json_encoder = CustomJSONEncoder


from . import views, models
