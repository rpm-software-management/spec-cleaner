#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup file for easy installation."""
from setuptools import setup
import glob
from spec_cleaner import __version__

setup(
    name='spec_cleaner',
    description='RPM .spec files cleaner',
    long_description='Command-line tool for cleaning various formatting ' +
        'errors in RPM .spec files',
    url='https://github.com/openSUSE/spec-cleaner',
    download_url='https://github.com/openSUSE/spec-cleaner',

    version=__version__,

    author='Tomáš Chvátal',
    author_email='tchvatal@suse.cz',

    maintainer='Tomáš Chvátal',
    maintainer_email='tchvatal@suse.cz',

    license='License :: OSI Approved :: BSD License',
    platforms=['Linux'],
    keywords=['SUSE', 'RPM', '.spec', 'cleaner'],

    tests_require=['mock', 'nose'],

    test_suite="nose.collector",

    packages=['spec_cleaner'],

    data_files=[
        ('lib/obs/service/', glob.glob('obs/*')),
        ('share/spec-cleaner', glob.glob('data/*')),
    ],

    entry_points={
        'console_scripts': ['spec-cleaner = spec_cleaner:main']},
)

