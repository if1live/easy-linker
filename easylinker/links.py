#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import os


def symlink(source, link_name):
    """
    http://stackoverflow.com/questions/6260149/os-symlink-support-in-windows
    """
    import os
    os_symlink = getattr(os, "symlink", None)
    if callable(os_symlink):
        os_symlink(source, link_name)
    else:
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        flags = 1 if os.path.isdir(source) else 0
        if csl(link_name, source, flags) == 0:
            raise ctypes.WinError()


class LinkException(Exception):
    pass

class Link(object):
    def __init__(self, src, dst):
        self.src = os.path.join(os.getcwd(), src)
        self.dst = dst

    def pathname_to_valid_pathname(self, pathname):
        return pathname.replace('/', os.path.sep).replace('\\', os.path.sep)

    def create(self):
        src = self.pathname_to_valid_pathname(self.src)
        dst = self.pathname_to_valid_pathname(self.dst)

        if os.path.exists(dst):
            msg = "Destination({}) is already exist.".format(dst)
            raise LinkException(msg)

        if not os.path.exists(src):
            msg = "Source({}) is not exist.".format(src)
            raise LinkException(msg)

        if os.path.isdir(src):
            self._process_directory(src, dst)
        else:
            self._process_file(src, dst)
        return True

    def _process_directory(self, src, dst):
        parent_dir = os.path.split(dst)[0]
        try:
            os.makedirs(parent_dir)
        except OSError:
            pass

        if os.name == 'nt':
            self._windows_directory_link(src, dst)
        else:
            self._unix_link(src, dst)

    def _process_file(self, src, dst):
        parent_dir = os.path.split(dst)[0]
        try:
            os.makedirs(parent_dir)
        except OSError:
            pass

        if os.name == 'nt':
            self._windows_file_link(src, dst)
        else:
            self._unix_link(src, dst)

    def _unix_link(self, src, dst):
        return os.symlink(src, dst)

    def _windows_file_link(self, src, dst):
        symlink(src, dst)

    def _windows_directory_link(self, src, dst):
        from ntfsutils import junction
        return junction.create(src, dst)
