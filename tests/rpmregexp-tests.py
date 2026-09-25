#!/usr/bin/env python

import time

from spec_cleaner.rpmregexp import Regexp


class TestRegexp:
    """We run few tests to ensure the regular expressions stay fast."""

    def test_long_rm_line(self):
        """Test that a long rm line without buildroot does not backtrack exponentially."""
        line = 'rm -rf ' + ' '.join(f'dir{i}' for i in range(20))
        start = time.perf_counter()
        assert not Regexp.re_clean.search(line)
        assert not Regexp.re_rm.search(line)
        assert time.perf_counter() - start < 1
