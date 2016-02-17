#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO


current_db_version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, current_db_version - 1)
print('Current database version: {}'.format(api.db_version(SQLALCHEMY_DATABASE_URI,
                                                           SQLALCHEMY_MIGRATE_REPO)))
