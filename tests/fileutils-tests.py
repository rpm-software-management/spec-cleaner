#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from spec_cleaner.fileutils import FileUtils
from spec_cleaner import RpmException


class TestFileutils(object):

    """
    We run few tests to ensure fileutils class works fine
    """

    def setup_class(self):
        """
        Declare global scope variables for further use.
        """
        self.fileutils = FileUtils()

    def test_open_assertion(self):
        with pytest.raises(RpmException):
            self.fileutils.open('missing-file.txt', 'r')

    def test_open_datafile_assertion(self):
        with pytest.raises(RpmException):
            self.fileutils.open_datafile('missing-file.txt')

    def test_open(self):
        self.fileutils.open('tests/fileutils-tests.py', 'r')
        self.fileutils.close()
        assert self.fileutils.f is None

    def test_open_datafile(self):
        self.fileutils.open_datafile('excludes-bracketing.txt')
        self.fileutils.close()
        assert self.fileutils.f is None
