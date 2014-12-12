#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import os

class IPath(object):
    def __call__(self):
        raise NotImplementedError()

class HomePath(IPath):
    def __call__(self):
        from os.path import expanduser
        return expanduser('~')

class MyDocumentPath(IPath):
    def __call__(self):
        if os.name == 'nt':
            return self._get_windows()
        else:
            return self._get_unix()

    def _get_windows(self):
        home_path = HomePath()
        return os.path.join(home_path(), 'Documents')

    def _get_unix(self):
        home_path = HomePath()
        return home_path()
