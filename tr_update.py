#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os


os.system('pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system('pybabel update -i messages.pot -d app/translations')
os.remove('messages.pot')
