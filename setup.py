#!/usr/bin/env python
#-*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

import os
import re

# https://github.com/zzzeek/sqlalchemy/blob/master/setup.py
v_file = open(os.path.join(os.path.dirname(__file__), 'easylinker', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)
v_file.close()

download_url = 'https://github.com/if1live/easylinker/tarball/{}'.format(VERSION)

packages = [
    'easylinker',
]

requires = [
    'https://github.com/if1live/ntfs.git#maste',
    'jinja2>=2.7.3',
]

tests_requires = [
    'nose>=1.3.4',
]

setup(
    name="easylinker",
    version=VERSION,
    url='https://github.com/if1live/easylinker',
    download_url=download_url,
    author="libsora",
    author_email="libsora25@gmail.com",
    maintainer="libsora",
    maintainer_email="libsora25@gmail.com",
    description="Tool for creating hard/symbolic link easily",
    long_description=open("README.rst").read(),
    license="MIT",
    packages=packages,
    package_data={'': ['LICENSE', ]},
    include_package_data=True,
    install_requires=requires,
    tests_require=tests_requires,
    keywords=['hardlink'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
