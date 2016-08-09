#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from setuptools import setup

setup(
    name = 'my_app',
    version = '1.0',
    license = 'GNU General Public License V3',
    author = 'wwd',
    author_email = '',
    description = 'Hello World application for flask',
    packages = ['my_app'],
    platforms = 'any',
    install_requires = [
        'flask',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
    ],
)
