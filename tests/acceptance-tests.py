#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import unittest
import os
import tempfile
import difflib
from spec_cleaner import RpmSpecCleaner

class TestCompare(unittest.TestCase):
    """
    We run individual tests to verify the content compared to expected results
    """

    def setUp(self):
        """
        Declare global scope variables for further use.
        """

        self.input_dir = self._get_input_dir()
        self.fixtures_dir = self._get_fixtures_dir()
        self.tmp_file = tempfile.NamedTemporaryFile()

    def _difftext(self, lines1, lines2, junk=None):
        junk = junk or (' ', '\t')
        # result is a generator
        result = difflib.ndiff(lines1, lines2, charjunk=lambda x: x in junk)
        read = []
        for line in result:
            read.append(line)
            # lines that don't start with a ' ' are diff ones
            if not line.startswith(' '):
                self.fail(''.join(read + list(result)))

    def assertStreamEqual(self, stream1, stream2, junk=None):
        """compare two streams (using difflib and readlines())"""
        # if stream2 is stream2, readlines() on stream1 will also read lines
        # in stream2, so they'll appear different, although they're not
        if stream1 is stream2:
            return
        # make sure we compare from the beginning of the stream
        stream1.seek(0)
        stream2.seek(0)
        # ocmpare
        self._difftext(stream1.readlines(), stream2.readlines(), junk)

    def _get_input_dir(self):
        """
        Return path for input files used by tests
        """
        return os.path.join(os.getcwd(), 'tests/in/')

    def _get_fixtures_dir(self):
        """
        Return path for representative output specs
        """
        return os.path.join(os.getcwd(), 'tests/out/')

    def _obtain_list_of_tests(self):
        """
        Generate list of tests we are going to use according to what is on hdd
        """

        test_files = list()

        for spec in os.listdir(self.fixtures_dir):
            if spec.endswith(".spec"):
                test_files.append(spec)

        return test_files

    def _run_individual_test(self, infile):
        """
        Run the cleaner as specified and store the output for further comparison.
        """
        cleaner = RpmSpecCleaner(infile, self.tmp_file.name, True, False, False, 'vimdiff')
        cleaner.run()

    def test_input_files(self):
        for test in self._obtain_list_of_tests():
            infile = os.path.join(self.input_dir, test)
            compare = os.path.join(self.fixtures_dir, test)

            self._run_individual_test(infile)

            self.assertStreamEqual(open(compare), open (self.tmp_file.name))
