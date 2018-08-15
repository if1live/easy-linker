#-*- coding: utf-8 -*-
#from __future__ import unicode_literals
#from __future__ import print_function

from jinja2 import Template
import re
import sys
from .config import PREDEFINED_VARIABLE_TABLE
from .links import Link, LinkException
import platform

class ParserException(Exception):
    pass


def to_unicode(val):
    if sys.version_info[0] == 2:
        return to_unicode_python2(val)
    else:
        return val

def to_unicode_python2(val):
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

class LineInfo(object):
    def __init__(self, success, src, dst, platform):
        self.success = success
        self.src = src
        self.dst = dst
        self.platform = platform

    def is_independent(self):
        return self.platform == None

    def is_win(self):
        if self.platform == None:
            return False
        WIN_PLATFORM_LIST = ['windows', 'win']
        return self.platform.lower() in WIN_PLATFORM_LIST

    def is_osx(self):
        if self.platform == None:
            return False
        OSX_PLATFORM_LIST = ['darwin', 'osx']
        return self.platform.lower() in OSX_PLATFORM_LIST

    def is_linux(self):
        if self.platform == None:
            return False
        LINUX_PLATFORM_LIST = ['linux']
        return self.platform.lower() in LINUX_PLATFORM_LIST

    @classmethod
    def invalid_line(cls):
        return LineInfo(False, None, None, None)
        
    def __eq__(self, o):
        return (
            self.success == o.success
            and self.src == o.src
            and self.dst == o.dst
            and self.platform == o.platform
        )
    

class LineParser(object):
    SIMPLE_PROG = re.compile(r'(?P<src>.+)->(?P<dst>.+)')
    PLATFORM_PROG = re.compile(r'(?P<platform>.+):(?P<src>.+)->(?P<dst>.+)')
    PROG_LIST = [
        PLATFORM_PROG,
        SIMPLE_PROG,
    ]

    def parse_simple(self, line):
        m = self.SIMPLE_PROG.match(line)
        if m:
            src = m.group('src').strip()
            dst = m.group('dst').strip()
            return LineInfo(True, src, dst, None)
        else:
            return LineInfo.invalid_line()

    def parse_platform(self, line):
        m = self.PLATFORM_PROG.match(line)
        if m:
            src = m.group('src').strip()
            dst = m.group('dst').strip()
            platform = m.group('platform').strip()
            return LineInfo(True, src, dst, platform)
        else:
            return LineInfo.invalid_line()

    def parse(self, line):
        line = line.strip()
        if not line:
            return LineInfo.invalid_line()

        if line[0] == '#':
            return LineInfo.invalid_line()

        line_info = None
        for prog in self.PROG_LIST:
            if prog == self.PLATFORM_PROG:
                line_info = self.parse_platform(line)
            elif prog == self.SIMPLE_PROG:
                line_info = self.parse_simple(line)

            if line_info.success:
                break

        if not line_info.success:
            raise ParserException('Not valid line [{}]'.format(line))

        if not line_info.src:
            raise ParserException('Empty src : [{}]'.format(line))
        if not line_info.dst:
            raise ParserException('Empty dst : [{}]'.format(line))

        return line_info
        
def read_textfile(filename):
    if sys.version_info[0] >= 3:
        return read_textfile_python3(filename)
    else:
        return read_textfile_python2(filename)
    
def read_textfile_python3(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        return content

def read_textfile_python2(filename):
    with open(filename, 'r') as f:
        content = f.read()
        content = to_unicode(content)
        assert type(content) == unicode
        return content

def run(filename):
    content = read_textfile(filename)
    var_converter = VariableConverter(PREDEFINED_VARIABLE_TABLE)
    content = var_converter.run(content)

    line_list = content.splitlines()

    curr_platform = platform.system().lower()
    line_parser = LineParser()
    for line in line_list:
        line_info = line_parser.parse(line)
        if not line_info.success:
            continue

        if line_info.is_win() and curr_platform != 'windows':
            continue
        if line_info.is_linux() and curr_platform != 'linux':
            continue
        if line_info.is_osx() and curr_platform != 'darwin':
            continue

        link = Link(line_info.src, line_info.dst)
        try:
            link.create()
        except LinkException as e:
            print(e.message)
