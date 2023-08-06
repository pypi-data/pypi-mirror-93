#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

from setuptools import setup, find_packages


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name="python-faasclient",
    url="https://gitlab.globoi.com/storm/python-faasclient",
    version=get_version("faasclient"),
    description='Python bindings to the Filer as a Service API.',
    author='STORM',
    author_email='storm@corp.globo.com',
    packages=find_packages(),
    install_requires=[
        'click>=6.2',
        'prettytable==0.7.2',
        'python-keystoneclient>=3.16.0',
        'requests>=2.19.1'
    ],
    entry_points={
        'console_scripts': [
            'faas = bin.commands:cli',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    zip_safe=False,
)
