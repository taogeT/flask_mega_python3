# -*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from .models import User


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not super().validate():
            return False
        if self.nickname.data == self.original_nickname:
            return True
        if User.query.filter_by(nickname=self.nickname.data).first():
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True


class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])


class SeachForm(Form):
    search = StringField('search', validators=[DataRequired()])
