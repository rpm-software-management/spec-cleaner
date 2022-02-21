#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from spec_cleaner import RpmExceptionError
from spec_cleaner.fileutils import open_datafile, open_stringio_spec


class TestFileutils(object):
    """We run few tests to ensure fileutils class works fine."""

    def test_open_assertion(self):
        """Test assert if file can be open with stringio."""
        with pytest.raises(RpmExceptionError):
            open_stringio_spec('missing-file.txt')

    def test_open_datafile_assertion(self):
        """Test opening file as datafile."""
        with pytest.raises(RpmExceptionError):
            open_datafile('missing-file.txt')

    def test_open(self):
        """Test open and closing file with stringio."""
        data = open_stringio_spec('tests/fileutils-tests.py')
        data.close()

    def test_open_datafile(self):
        """Test open and closing file with datafile."""
        data = open_datafile('excludes-bracketing.txt')
        data.close()
