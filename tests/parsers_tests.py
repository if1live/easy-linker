#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import unittest
from easylinker import parsers

class VariableConverterTest(unittest.TestCase):
    VAR_TABLE = {
        'A': 'foo',
        'B': 'bar',
    }
    def test_success(self):
        template = "{{A}} is {{B}}"
        converter = parsers.VariableConverter(self.VAR_TABLE)
        actual = converter.run(template)
        expected = "foo is bar"
        assert actual == expected


class LineParserTest(unittest.TestCase):
    def test_valid(self):
        line_list = [
            'a -> b',
            'a->b',
            '   a  ->   b   ',
        ]
        line_parser = parsers.LineParser()
        for line in line_list:
            actual = line_parser.parse(line)
            assert actual == parsers.LineInfo(True, 'a', 'b', None)

    def test_platform(self):
        line_parser = parsers.LineParser()
        line = 'platform: a -> b'
        actual = line_parser.parse(line)
        assert actual == parsers.LineInfo(True, 'a', 'b', 'platform')

    def test_comment(self):
        line_parser = parsers.LineParser()
        actual = line_parser.parse('# this is comment')
        assert actual == parsers.LineInfo(False, None, None, None)

    def test_empty_line(self):
        line_parser = parsers.LineParser()
        actual = line_parser.parse('         ')
        assert actual == parsers.LineInfo(False, None, None, None)

    def test_not_valid(self):
        line_parser = parsers.LineParser()
        line_list = [
            'a ->',
            ' -> b',
            'a - > b',
            'a => b'
        ]
        for line in line_list:
            with self.assertRaises(parsers.ParserException) as cm:
                line_parser.parse(line)
