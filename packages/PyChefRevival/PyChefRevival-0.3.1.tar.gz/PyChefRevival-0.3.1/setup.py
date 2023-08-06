#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os

from setuptools import setup, find_packages

setup(
    name='PyChefRevival',
    version='0.3.1',
    packages=find_packages(),
    author='Aryn Lacy',
    author_email='aryn.lacy@gmail.com',
    description='Python implementation of a Chef API client.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license='Apache 2.0',
    keywords='',
    url='http://github.com/aryn-lacy/pychef',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    install_requires=['six>=1.9.0', 'requests>=2.7.0'],
    tests_require=['unittest2', 'mock'],
    test_suite='unittest2.collector',
)
