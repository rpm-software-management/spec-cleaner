"""
Acceptance tests module.

In this module we run all the tests to ensure the spec-cleaner is acting sanely.
"""


import os
from glob import glob
from shutil import copyfile

import pytest

from spec_cleaner import RpmExceptionError, RpmSpecCleaner


def collect_tests(directory):
    """
    Generate a list of tests we are going to use according to what is on hdd.

    Args:
        directory: A string representing a directory with tests.

    Return:
        A list with test names in the given directory.
    """
    testglob = os.path.join('tests', directory, '*.spec')
    return [os.path.basename(f) for f in glob(testglob)]


class TestCompare(object):
    """
    We run individual tests to verify the content compared to expected results.

    All input test files are stored in 'in' directory. Then the test outputs are divided to categories in separate
    output directories:

    E.g.:
      * 'out' - all outputs (no particular spec-cleaner option is used),
      * 'out-minimal' - outputs for tests using '--minimal' option,
      * 'web' - outputs for tests requiring internet connection,
      * 'tex', 'perl', 'cmake' - outputs for tests using '--tex', '--perl' or '--cmake' option,
      ...

    These output directories are used to help collect and run tests with the same parameters.
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
        'remove_groups': False,
        'tex': False,
        'perl': False,
        'cmake': False,
        'keep_space': False,
    }

    @pytest.fixture(scope='function')
    def tmpfile(self, tmpdir_factory):
        """Create empty temp folder for each function run to avoid clash in threaded execution."""
        tmpfile = tmpdir_factory.mktemp('run', numbered=True).join('testing.spec')
        return str(tmpfile)

    def _run_individual_test(self, test, compare_dir, infile=None, outfile=None, options=None):
        """Run the cleaner as specified and store the output for further comparison."""
        if not infile:
            infile = os.path.join('tests', 'in', test)

        full_options = {'specfile': infile, 'output': outfile}
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

    @pytest.mark.parametrize('test', collect_tests('out'))
    def test_normal_outputs(self, tmpfile, test):
        """Run all tests in 'out' directory without any particular spec-cleaner option."""
        self._compare_and_rerun(test, 'out', tmpfile, {'pkgconfig': True})

    @pytest.mark.parametrize('test', collect_tests('out-minimal'))
    def test_minimal_outputs(self, test, tmpfile):
        """Run tests in 'out-minimal' directory in a minimal mode."""
        self._compare_and_rerun(test, 'out-minimal', tmpfile, {'pkgconfig': True, 'minimal': True})

    @pytest.mark.parametrize('test', collect_tests('keep-space'))
    def test_keep_space_output(self, tmpfile, test):
        """Run tests in 'keep-space' directory with '--keep-space' option."""
        self._compare_and_rerun(test, 'keep-space', tmpfile, options={'keep_space': True})

    @pytest.mark.webtest
    @pytest.mark.parametrize('test', collect_tests('web'))
    def test_web_output(self, tmpfile, test):
        """Run tests in 'web' directory (these tests need an internet connection)."""
        self._compare_and_rerun(test, 'web', tmpfile, {'pkgconfig': True})

    def test_inline_function(self, tmpfile):
        """Test an inline option."""
        test = 'bconds.spec'
        infile = os.path.join('tests', 'in', test)
        copyfile(infile, tmpfile)
        self._run_individual_test(
            test, None, infile=tmpfile, outfile='', options={'pkgconfig': True, 'inline': True}
        )

    def test_diff_function(self, tmpfile):
        """Test passing an incorrect '--diff_prog' option."""
        test = 'bconds.spec'
        with pytest.raises(RpmExceptionError):
            self._run_individual_test(
                test, None, outfile='', options={'diff': True, 'diff_prog': 'error'}
            )

    def test_unicode(self, tmpfile):
        """Test encoding."""
        test = 'perl-Text-Unidecode.spec'
        testpath = os.path.join('tests', 'unicode', test)
        with pytest.raises(RpmExceptionError):
            self._run_individual_test(
                test, None, infile=testpath, outfile='', options={'minimal': False}
            )

    @pytest.mark.parametrize(
        'test, compare_dir, options',
        [
            ('header.spec', 'header', {'minimal': True, 'no_copyright': False}),
            ('pkgconfrequires.spec', 'out', {'pkgconfig': False}),
            ('tex.spec', 'tex', {'tex': True}),
            ('perl.spec', 'perl', {'perl': True}),
            ('cmake.spec', 'cmake', {'cmake': True}),
            ('langpackage.spec', 'group', {'remove_groups': True}),
        ],
    )
    def test_single_output(self, tmpfile, test, compare_dir, options):
        """Test various spec-cleaner options."""
        self._run_individual_test(test, compare_dir, outfile=tmpfile, options=options)
