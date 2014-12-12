#-*- coding: utf-8 -*-
#from __future__ import unicode_literals
#from __future__ import print_function

from jinja2 import Template
import re
from config import PREDEFINED_VARIABLE_TABLE
from links import Link

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

        assert type(src) == unicode
        assert type(dst) == unicode
        return src, dst

def run(filename):
    with open(filename, 'rb') as f:
        content = f.read()
        content = to_unicode(content)
        assert type(content) == unicode

    var_converter = VariableConverter(PREDEFINED_VARIABLE_TABLE)
    content = var_converter.run(content)

    line_list = content.splitlines()

    line_parser = LineParser()
    for line in line_list:
        src, dst = line_parser.parse(line)
        link = Link(src, dst)
        link.create()
