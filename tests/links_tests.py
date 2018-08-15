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
        src_f.write("dummy data".encode("utf-8"))
        src_f.close()
        src = src_f.name
        dst = create_not_exist_filename()

        assert True == os.path.exists(src)
        assert False == os.path.exists(dst)
        assert True == os.path.isfile(src)

        # run logic
        link = links.Link(src, dst)
        link.create()

        # assert
        assert True == os.path.exists(src)
        assert True == os.path.exists(dst)
        assert True == os.path.isfile(src)
        assert True == os.path.isfile(dst)

        with open(src, 'rb') as f:
            src_content = f.read()
        with open(dst, 'rb') as f:
            assert src_content == f.read()

        # tear down fixture
        os.unlink(src)
        os.unlink(dst)
        assert False == os.path.exists(src)
        assert False == os.path.exists(dst)


class Link_directory_link_Test(unittest.TestCase):
    def test_directory(self):
        # set up fixture
        src = tempfile.mkdtemp()
        dst = src + '-test'
        assert True == os.path.exists(src)
        assert False == os.path.exists(dst)
        assert True == os.path.isdir(src)

        link = links.Link(src, dst)
        link.create()

        # assert
        assert True == os.path.exists(src)
        assert True == os.path.exists(dst)
        assert True == os.path.isdir(src)
        assert True == os.path.isdir(dst)

        # tear down fixture
        try:
            os.removedirs(src)
        except OSError:
            pass
        try:
            os.removedirs(dst)
        except OSError:
            pass

        assert False == os.path.exists(src)
        assert False == os.path.exists(dst)


class Link_src_not_exist_Test(unittest.TestCase):
    def test_src_not_exist(self):
        src = create_not_exist_filename()
        dst = create_not_exist_filename()
        assert False == os.path.exists(src)
        assert False == os.path.exists(dst)

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
