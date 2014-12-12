#-*- coding: utf-8 -*-__doc__

from __future__ import unicode_literals
from __future__ import print_function

import os
import unittest
from easylinker import pathlib

class HomePathTest(unittest.TestCase):
    def test_call(self):
        home_path = pathlib.HomePath()
        pathname = home_path()
        #print('home path : {}'.format(pathname))
        self.assertEqual(True, os.path.exists(pathname))
        self.assertEqual(True, os.path.isdir(pathname))

class MyDocumentPathTest(unittest.TestCase):
    def test_call(self):
        doc_path = pathlib.MyDocumentPath()
        pathname = doc_path()
        #print('my document path : {}'.format(pathname))
        self.assertEqual(True, os.path.exists(pathname))
        self.assertEqual(True, os.path.isdir(pathname))
