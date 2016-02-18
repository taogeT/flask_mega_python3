# -*- coding: UTF-8 -*-
from hashlib import md5
from . import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=Followers.table,
                               primaryjoin=(Followers.table.c.follower_id == id),
                               secondaryjoin=(Followers.table.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def avatar(self, size):
        return 'https://gravatar.duoshuo.com/avatar/{}?d=mm&s={}'.format(md5(self.email.encode('utf-8')).hexdigest(), size)

    @staticmethod
    def make_unique_nickname(nickname):
        if not User.query.filter_by(nickname=nickname).first():
            return nickname
        version = 2
        while True:
            new_nickname = '{}{}'.format(nickname, version)
            if not User.query.filter_by(nickname=new_nickname).first():
                return new_nickname
            version += 1

    def __repr__(self):
        return '<User {}>'.format(self.nickname)


class Followers(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
