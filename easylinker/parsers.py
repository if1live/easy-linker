#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from jinja2 import Template
import re


class ParserException(Exception):
    pass


def to_unicode(val):
    if type(val) == unicode:
        return val

    elif type(val) == str:
        try:
            return val.decode('utf-8')
        except UnicodeDecodeError:
            return val.decode('euc-kr')
    else:
        raise AssertionError('not valid type')

class VariableConverter(object):
    def __init__(self, var_table):
        self.var_table = var_table

    def run(self, text):
        template = Template(
            text,
        )
        output = template.render(**self.var_table)
        return output

class LineParser(object):
    PROG = re.compile(r'(?P<src>.+)->(?P<dst>.+)')

    def parse(self, line):
        m = self.PROG.match(line)
        if not m:
            raise ParserException('Not valid line : {}'.format(line))

        src = m.group('src').strip()
        dst = m.group('dst').strip()

        if not src:
            raise ParserException('Empty src : {}'.format(line))
        if not dst:
            raise ParserException('Empty dst : {}'.format(line))

        return src, dst
