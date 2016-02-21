# -*- coding: UTF-8 -*-
import os


CSRF_ENABLED = True
SECRET_KEY = 'xxxxxxxx'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'OpenIDCN', 'url': 'http://<username>.openid.org.cn'}
]

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['you@example.com']

# pagination
POSTS_PER_PAGE = 3

# available languages
LANGUAGES = {'en': 'English', 'zh': '中文简体'}
