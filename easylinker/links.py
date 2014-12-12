#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import os


class LinkException(Exception):
    pass

class Link(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def create(self):
        src = self.src
        dst = self.dst

        if os.path.exists(dst):
            msg = "Destination({}) is already exist.".format(dst)
            raise LinkException(msg)

        if not os.path.exists(src):
            msg = "Source({}) is not exist.".format(src)
            raise LinkException(msg)

        if os.name == 'nt':
            if os.path.isdir(src):
                self._windows_directory_link(src, dst)
            else:
                self._windows_file_link(src, dst)
        else:
            self._unix_link(src, dst)

        return True

    def _unix_link(self, src, dst):
        return os.symlink(src, dst)

    def _windows_file_link(self, src, dst):
        from ntfsutils import hardlink
        return hardlink.create(src, dst)

    def _windows_directory_link(self, src, dst):
        from ntfsutils import junction
        return junction.create(src, dst)
