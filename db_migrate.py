#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from app import db
import imp


next_db_version = api.db_version(SQLALCHEMY_DATABASE_URI,
                                 SQLALCHEMY_MIGRATE_REPO) + 1
migration = '{}/versions/{:0>3}_migration.py'.format(SQLALCHEMY_MIGRATE_REPO,
                                                 next_db_version)
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                          SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, db.metadata)
with open(migration, 'wt') as mgpy:
    mgpy.write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as {}'.format(migration))
print('Current database version: {}'.format(api.db_version(SQLALCHEMY_DATABASE_URI,
                                                           SQLALCHEMY_MIGRATE_REPO)))
