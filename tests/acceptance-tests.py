#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import shutil
import tempfile
import difflib
import datetime
from nose.tools import raises

from spec_cleaner import RpmException
from spec_cleaner import RpmSpecCleaner


class NewDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2013, 1, 1)

datetime.date = NewDate

class TestCompare(object):

    """
    We run individual tests to verify the content compared to expected results
    """

    option_presets = {
        'pkgconfig': False,
        'inline': False,
        'diff': False,
        'diff_prog': 'vimdiff',
        'minimal': False,
        'no_curlification': False,
        'no_copyright': True,
        'tex': False,
        'perl': False,
        'cmake': False,
        'keep_space': False,
    }

    def _difftext(self, lines1, lines2, junk=None):
        junk = junk or (' ', '\t')
        # result is a generator
        result = difflib.ndiff(lines1, lines2, charjunk=lambda x: x in junk)
        read = []
        for line in result:
            read.append(line)
            # lines that don't start with a ' ' are diff ones
            if not line.startswith(' '):
                assert False, ''.join(read + list(result))

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

    def _list_tests(self, directory='in'):
        """
        Generate list of tests we are going to use according to what is on hdd
        """
        testglob = os.path.join('tests', directory, '*.spec')
        return [os.path.basename(f) for f in glob.glob(testglob)]

    def _run_individual_test(self, test, compare_dir, infile=None, outfile=None, options=None, **kwargs):
        """
        Run the cleaner as specified and store the output for further comparison.
        """
        with tempfile.NamedTemporaryFile() as default_tmp_file:
            if infile is None:
                infile = os.path.join('tests', 'in', test)

            if outfile is None:
                outfile = default_tmp_file.name

            full_options = {
                'specfile': infile,
                'output': outfile,
            }
            full_options.update(self.option_presets)
            full_options.update(kwargs)
            full_options.update(options or {})

            cleaner = RpmSpecCleaner(full_options)
            cleaner.run()

            if compare_dir is not None:
                compare  = os.path.join('tests', compare_dir, test)
                testfile = full_options['inline'] and infile or outfile
                with open(compare) as ref, open(testfile) as test:
                    self.assertStreamEqual(ref, test)

    def _compare_and_rerun(self, compare_dir, **kwargs):
        for test in self._list_tests():
            with tempfile.NamedTemporaryFile(suffix="-"+test) as tmpfile:
                tmp = tmpfile.name
                yield self._run_individual_test, test, compare_dir, None, tmp, kwargs
                yield self._run_individual_test, test, compare_dir, tmp, None, kwargs

    def test_normal_outputs(self):
        for testcase in self._compare_and_rerun('out', pkgconfig=True):
            yield testcase

    def test_minimal_outputs(self):
        for testcase in self._compare_and_rerun('out-minimal', pkgconfig=True, minimal=True):
            yield testcase

    def test_copyright_output(self):
        self._run_individual_test('header.spec', 'header', minimal=True, no_copyright=False)

    def test_keep_space_output(self):
        for test in self._list_tests('keep-space'):
            self._run_individual_test(test, 'keep-space', keep_space=True)

    def test_pkgconfig_disabled_output(self):
        self._run_individual_test('pkgconfrequires.spec', 'out', pkgconfig=False)

    def test_inline_function(self):
        test = self._list_tests()[0]
        infile = os.path.join('tests', 'in', test)
        with tempfile.NamedTemporaryFile() as tmpfile:
            shutil.copyfile(infile, tmpfile.name)
            self._run_individual_test(test, None,
                    infile=tmpfile.name, outfile='',
                    pkgconfig=True, inline=True)

    def test_regular_output(self):
        test = self._list_tests()[0]
        self._run_individual_test(test, None, outfile='')

    @raises(RpmException)
    def test_diff_function(self):
        test = self._list_tests()[0]
        self._run_individual_test(test, None, outfile='', diff=True, diff_prog='error')

    def test_tex_output(self):
        self._run_individual_test('tex.spec', 'tex', tex=True)

    def test_perl_output(self):
        self._run_individual_test('perl.spec', 'perl', perl=True)

    def test_cmake_output(self):
        self._run_individual_test('cmake.spec', 'cmake', cmake=True)
