#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
import tempfile
import difflib
import datetime
from mock import patch

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
        self.minimal_fixtures_dir = self._get_minimal_fixtures_dir()
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_file_rerun = tempfile.NamedTemporaryFile()

    def tearDown(self):
        """
        Remove the tmp directory
        """
        shutil.rmtree(self.tmp_dir)

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

    def _get_minimal_fixtures_dir(self):
        """
        Return path for representative output specs
        """
        return os.path.join(os.getcwd(), 'tests/out-minimal/')

    def _obtain_list_of_tests(self):
        """
        Generate list of tests we are going to use according to what is on hdd
        """
        test_files = list()

        for spec in os.listdir(self.fixtures_dir):
            if spec.endswith(".spec"):
                test_files.append(spec)

        return test_files

    def _run_individual_test(self, options):
        """
        Run the cleaner as specified and store the output for further comparison.
        """
        cleaner = RpmSpecCleaner(options)
        cleaner.run()

    @patch('spec_cleaner.rpmcopyright.datetime')
    def test_input_files(self, datetime_mock):
        datetime_mock.datetime.now.return_value = (
            datetime.datetime(2013, 1, 1))
        for test in self._obtain_list_of_tests():
            infile = os.path.join(self.input_dir, test)
            compare = os.path.join(self.fixtures_dir, test)
            tmp_file = os.path.join(self.tmp_dir, test)

            # first try to generate cleaned content from messed up
            options = {
                'specfile': infile,
                'output': tmp_file,
                'pkgconfig': True,
                'inline': False,
                'diff': False,
                'diff_prog': 'vimdiff',
                'minimal': False,
                'no_copyright': False,
            }
            self._run_individual_test(options)
            with open(compare) as ref, open(tmp_file) as test:
                self.assertStreamEqual(ref, test)

            # second run it again while ensuring it didn't change
            options = {
                'specfile': tmp_file,
                'output': self.tmp_file_rerun.name,
                'pkgconfig': True,
                'inline': False,
                'diff': False,
                'diff_prog': 'vimdiff',
                'minimal': False,
                'no_copyright': False,
            }
            self._run_individual_test(options)
            with open(compare) as ref, open(self.tmp_file_rerun.name) as test:
                self.assertStreamEqual(ref, test)

    @patch('spec_cleaner.rpmcopyright.datetime')
    def test_minimal_output(self, datetime_mock):
        datetime_mock.datetime.now.return_value = (
            datetime.datetime(2013, 1, 1))
        for test in self._obtain_list_of_tests():
            infile = os.path.join(self.input_dir, test)
            compare = os.path.join(self.minimal_fixtures_dir, test)
            tmp_file = os.path.join(self.tmp_dir, test)

            # first try to generate cleaned content from messed up
            options = {
                'specfile': infile,
                'output': tmp_file,
                'pkgconfig': True,
                'inline': False,
                'diff': False,
                'diff_prog': 'vimdiff',
                'minimal': True,
                'no_copyright': False,
            }
            self._run_individual_test(options)
            with open(compare) as ref, open(tmp_file) as test:
                self.assertStreamEqual(ref, test)

            # second run it again while ensuring it didn't change
            options = {
                'specfile': tmp_file,
                'output': self.tmp_file_rerun.name,
                'pkgconfig': True,
                'inline': False,
                'diff': False,
                'diff_prog': 'vimdiff',
                'minimal': True,
                'no_copyright': False,
            }
            self._run_individual_test(options)
            with open(compare) as ref, open(self.tmp_file_rerun.name) as test:
                self.assertStreamEqual(ref, test)

    @patch('spec_cleaner.rpmcopyright.datetime')
    def test_no_copyright_output(self, datetime_mock):
        datetime_mock.datetime.now.return_value = (
            datetime.datetime(2013, 1, 1))
        spec_str="""%check
make check

%changelog
"""
        tmp_file = os.path.join(self.tmp_dir, "no_copyright_test.spec")
        out_file = os.path.join(self.tmp_dir, "no_copyright_test_out.spec")
        with open(tmp_file, "w+") as t:
            t.write(spec_str)

        # first try to generate cleaned content from messed up
        options = {
            'specfile': tmp_file,
            'output': out_file,
            'pkgconfig': True,
            'inline': False,
            'diff': False,
            'diff_prog': 'vimdiff',
            'minimal': True,
            'no_copyright': True,
        }
        self._run_individual_test(options)
        with open(out_file) as ref, open(tmp_file) as test:
            self.assertStreamEqual(ref, test)

    @patch('spec_cleaner.rpmcopyright.datetime')
    def test_inline_function(self, datetime_mock):
        datetime_mock.datetime.now.return_value = (
            datetime.datetime(2013, 1, 1))

        test = self._obtain_list_of_tests()[0]
        infile = os.path.join(self.input_dir, test)
        compare = os.path.join(self.fixtures_dir, test)
        tmp_file = os.path.join(self.tmp_dir, test)
        shutil.copyfile(infile, tmp_file)

        options = {
            'specfile': tmp_file,
            'output': '',
            'pkgconfig': True,
            'inline': True,
            'diff': False,
            'diff_prog': 'vimdiff',
            'minimal': False,
            'no_copyright': False,
        }
        self._run_individual_test(options)
        with open(compare) as ref, open(tmp_file) as test:
            self.assertStreamEqual(ref, test)

    @patch('spec_cleaner.rpmcopyright.datetime')
    def test_regular_output(self, datetime_mock):
        datetime_mock.datetime.now.return_value = (
            datetime.datetime(2013, 1, 1))

        test = self._obtain_list_of_tests()[0]
        infile = os.path.join(self.input_dir, test)
        options = {
            'specfile': infile,
            'output': '',
            'pkgconfig': True,
            'inline': False,
            'diff': False,
            'diff_prog': 'gvimdiff',
            'minimal': False,
            'no_copyright': False,
        }
        self._run_individual_test(options)

    @patch('spec_cleaner.rpmcopyright.datetime')
    @patch('subprocess.call')
    def test_diff_function(self, datetime_mock, subprocess_mock):
        datetime_mock.datetime.now.return_value = (
            datetime.datetime(2013, 1, 1))
        subprocess_mock.subprocess.call.return_value = True

        test = self._obtain_list_of_tests()[0]
        infile = os.path.join(self.input_dir, test)
        options = {
            'specfile': infile,
            'output': '',
            'pkgconfig': True,
            'inline': False,
            'diff': True,
            'diff_prog': 'gvimdiff',
            'minimal': False,
            'no_copyright': False,
        }
        self._run_individual_test(options)
