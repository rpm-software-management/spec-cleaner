#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from spec_cleaner import RpmException
from spec_cleaner.fileutils import open_datafile, open_stringio_spec


class TestFileutils(object):

    """
    We run few tests to ensure fileutils class works fine
    """

    def test_open_assertion(self):
        with pytest.raises(RpmException):
            open_stringio_spec('missing-file.txt')

    def test_open_datafile_assertion(self):
        with pytest.raises(RpmException):
            open_datafile('missing-file.txt')

    def test_open(self):
        data = open_stringio_spec('tests/fileutils-tests.py')
        data.close()

    def test_open_datafile(self):
        data = open_datafile('excludes-bracketing.txt')
        data.close()
