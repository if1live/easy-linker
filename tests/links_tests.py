#-*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os
import tempfile
import unittest
from easylinker import links


def create_not_exist_filename():
    f = tempfile.NamedTemporaryFile(delete=False)
    filepath = f.name
    f.close()
    os.unlink(filepath)
    assert False == os.path.exists(filepath)
    return filepath


class Link_file_link_Test(unittest.TestCase):
    def test_file(self):
        # setup fixture
        src_f = tempfile.NamedTemporaryFile(delete=False)
        src_f.write('dummy data')
        src_f.close()
        src = src_f.name
        dst = create_not_exist_filename()

        self.assertEqual(True, os.path.exists(src))
        self.assertEqual(False, os.path.exists(dst))
        self.assertEqual(True, os.path.isfile(src))

        # run logic
        link = links.Link(src, dst)
        link.create()

        # assert
        self.assertEqual(True, os.path.exists(src))
        self.assertEqual(True, os.path.exists(dst))
        self.assertEqual(True, os.path.isfile(src))
        self.assertEqual(True, os.path.isfile(dst))
        self.assertEqual(True, os.path.getsize(src) > 0)
        self.assertEqual(os.path.getsize(src), os.path.getsize(dst))

        # tear down fixture
        os.unlink(src)
        os.unlink(dst)
        self.assertEqual(False, os.path.exists(src))
        self.assertEqual(False, os.path.exists(dst))


class Link_directory_link_Test(unittest.TestCase):
    def test_directory(self):
        # set up fixture
        src = tempfile.mkdtemp()
        dst = src + '-test'
        self.assertEqual(True, os.path.exists(src))
        self.assertEqual(False, os.path.exists(dst))
        self.assertEqual(True, os.path.isdir(src))

        link = links.Link(src, dst)
        link.create()

        # assert
        self.assertEqual(True, os.path.exists(src))
        self.assertEqual(True, os.path.exists(dst))
        self.assertEqual(True, os.path.isdir(src))
        self.assertEqual(True, os.path.isdir(dst))

        # tear down fixture
        os.removedirs(src)
        os.removedirs(dst)
        self.assertEqual(False, os.path.exists(src))
        self.assertEqual(False, os.path.exists(dst))


class Link_src_not_exist_Test(unittest.TestCase):
    def test_src_not_exist(self):
        src = create_not_exist_filename()
        dst = create_not_exist_filename()
        self.assertEqual(False, os.path.exists(src))
        self.assertEqual(False, os.path.exists(dst))

        link = links.Link(src, dst)
        with self.assertRaises(links.LinkException) as cm:
            link.create()

class Link_dst_already_exist_Test(unittest.TestCase):
    def test_dst_already_exist(self):
        src = tempfile.NamedTemporaryFile(delete=True)
        dst = tempfile.NamedTemporaryFile(delete=True)

        link = links.Link(src.name, dst.name)
        with self.assertRaises(links.LinkException) as cm:
            link.create()
