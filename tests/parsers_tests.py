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
        self.assertEqual(actual, expected)


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
            self.assertEqual(True, actual.success)
            self.assertEqual('a', actual.src)
            self.assertEqual('b', actual.dst)
            self.assertEqual(None, actual.platform)

    def test_platform(self):
        line_parser = parsers.LineParser()
        line = 'platform: a -> b'
        actual = line_parser.parse(line)
        self.assertEqual(True, actual.success)
        self.assertEqual('a', actual.src)
        self.assertEqual('b', actual.dst)
        self.assertEqual('platform', actual.platform)

    def test_comment(self):
        line_parser = parsers.LineParser()
        actual = line_parser.parse('# this is comment')
        self.assertEqual(False, actual.success)
        self.assertEqual(None, actual.src)
        self.assertEqual(None, actual.dst)
        self.assertEqual(None, actual.platform)

    def test_empty_line(self):
        line_parser = parsers.LineParser()
        actual = line_parser.parse('         ')
        self.assertEqual(False, actual.success)
        self.assertEqual(None, actual.src)
        self.assertEqual(None, actual.dst)
        self.assertEqual(None, actual.platform)

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
