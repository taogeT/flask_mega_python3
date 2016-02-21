#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys


if len(sys.argv) != 2:
    print('usage: tr_init <language-code>')
    sys.exit(1)
os.system('pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system('pybabel init -i messages.pot -d app/translations -l {}'.format(sys.argv[1]))
os.remove('messages.pot')
