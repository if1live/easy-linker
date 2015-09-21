#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from . import pathlib

PREDEFINED_VARIABLE_TABLE = {
    'HOME': pathlib.HomePath()(),
    'MYDOC': pathlib.MyDocumentPath()(),
}
