#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from config import basedir
from app import app, db
from app.models import User

import os
import unittest


class MegaTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'tmp', 'test.db'))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_make_unique_nickname(self):
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname(nickname='john')
        assert nickname != 'john'
        u = User(nickname='susan', email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname(nickname='john')
        assert nickname2 != 'john'
        assert nickname2 == nickname


if __name__ == '__main__':
    unittest.main()





