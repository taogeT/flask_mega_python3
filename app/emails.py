# -*- coding: UTF-8 -*-
from flask import render_template
from flask.ext.mail import Message
from flask.ext.babel import gettext
from . import mail, app
from .decorators import async


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)


def follower_notification(followed, follower):
    send_email(subject=gettext('[microblog] %(nickname)s is now following you!', nickname=follower.nickname),
               sender=app.config['ADMINS'][0],
               recipients=[followed.email],
               text_body=render_template('follower_email.txt',
                                         user=followed, follower=follower),
               html_body=render_template('follower_email.html',
                                         user=followed, follower=follower))
