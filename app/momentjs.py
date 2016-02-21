# -*- coding: UTF-8 -*-
from jinja2 import Markup


class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, formatter):
        timestampstr = self.timestamp.strftime('%Y-%m-%dT%H:%M:%S Z')
        return Markup('<script>document.write(moment("{}").{});</script>'.format(timestampstr, formatter))

    def format(self, fmt):
        return self.render('format("{}")'.format(fmt))

    def calendar(self):
        return self.render('calendar()')

    def fromNow(self):
        return self.render('fromNow()')
