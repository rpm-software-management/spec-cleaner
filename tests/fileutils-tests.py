#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import raises

from spec_cleaner.fileutils import FileUtils
from spec_cleaner import RpmException

class TestFileutils(unittest.TestCase):

    """
    We run few tests to ensure fileutils class works fine
    """

    def setUp(self):
        """
        Declare global scope variables for further use.
        """
        self.fileutils = FileUtils()

    @raises(RpmException)
    def test_open_assertion(self):
        self.fileutils.open('missing-file.txt', 'r')

    @raises(RpmException)
    def test_open_datafile_assertion(self):
        self.fileutils.open_datafile('missing-file.txt')

    def test_open(self):
        self.fileutils.open('tests/fileutils-tests.py', 'r')
        self.fileutils.close()
        self.assertEqual(None, self.fileutils.f)

    def test_open_datafile(self):
        self.fileutils.open_datafile('excludes-bracketing.txt')
        self.fileutils.close()
        self.assertEqual(None, self.fileutils.f)
