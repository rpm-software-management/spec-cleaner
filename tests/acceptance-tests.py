#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
from shutil import copyfile
import pytest

from spec_cleaner import RpmException
from spec_cleaner import RpmSpecCleaner


@pytest.fixture(scope='session')
def tests():
    """
    Generate list of tests we are going to use according to what is on hdd
    """
    testglob = os.path.join('tests', 'in', '*.spec')
    return [os.path.basename(f) for f in glob.glob(testglob)]


@pytest.fixture(scope='session')
def space_tests():
    """
    Generate list of tests we are going to use according to what is on hdd
    """
    testglob = os.path.join('tests', 'keep-space', '*.spec')
    return [os.path.basename(f) for f in glob.glob(testglob)]


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
        'copyright_year': 2013,
        'tex': False,
        'perl': False,
        'cmake': False,
        'keep_space': False,
    }

    @pytest.fixture(scope='function')
    def tmpfile(self, tmpdir_factory):
        tmpfile = tmpdir_factory.mktemp('run', numbered=True).join('testing.spec')
        return str(tmpfile)

    def _run_individual_test(self, test, compare_dir, infile=None, outfile=None, options=None):
        """
        Run the cleaner as specified and store the output for further comparison.
        """
        if not infile:
            infile = os.path.join('tests', 'in', test)

        full_options = {
            'specfile': infile,
            'output': outfile,
        }
        full_options.update(self.option_presets)
        full_options.update(options)

        cleaner = RpmSpecCleaner(full_options)
        cleaner.run()

        if compare_dir:
            compare = os.path.join('tests', compare_dir, test)
            testfile = full_options['inline'] and infile or outfile
            with open(compare) as ref, open(testfile) as test:
                assert ref.read() == test.read()

    def _compare_and_rerun(self, test, compare_dir, tmpfile, options=None):
        self._run_individual_test(test, compare_dir, None, tmpfile, options)
        tmpfile_rerun = tmpfile + '_rerun'
        self._run_individual_test(test, compare_dir, tmpfile, tmpfile_rerun, options)

    @pytest.mark.parametrize('test', tests())
    def test_normal_outputs(self, tmpfile, test):
        self._compare_and_rerun(test, 'out', tmpfile, {'pkgconfig': True})

    @pytest.mark.parametrize('test', tests())
    def test_minimal_outputs(self, test, tmpfile):
        self._compare_and_rerun(test, 'out-minimal', tmpfile, {'pkgconfig': True, 'minimal': True})

    @pytest.mark.parametrize('test', space_tests())
    def test_keep_space_output(self, tmpfile, test):
        self._compare_and_rerun(test, 'keep-space', tmpfile, options={'keep_space': True})

    def test_inline_function(self, tmpfile):
        test = 'bconds.spec'
        infile = os.path.join('tests', 'in', test)
        copyfile(infile, tmpfile)
        self._run_individual_test(test, None, infile=tmpfile, outfile='', options={'pkgconfig': True, 'inline': True})

    def test_diff_function(self, tmpfile):
        test = 'bconds.spec'
        with pytest.raises(RpmException):
            self._run_individual_test(test, None, outfile='', options={'diff': True, 'diff_prog': 'error'})

    @pytest.mark.parametrize(
        'test, compare_dir, options',
        [
            ('header.spec', 'header', {'minimal': True, 'no_copyright': False}),
            ('pkgconfrequires.spec', 'out', {'pkgconfig': False}),
            ('tex.spec', 'tex', {'tex': True}),
            ('perl.spec', 'perl', {'perl': True}),
            ('cmake.spec', 'cmake', {'cmake': True}),
        ]
    )
    def test_single_output(self, tmpfile, test, compare_dir, options):
        self._run_individual_test(test, compare_dir, outfile=tmpfile, options=options)
