#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmpreambleelements import RpmPreambleElements


def _default_options(tmp_path):
    """Create the default options dict for tests."""
    specfile = tmp_path / 'test.spec'
    specfile.write_text('Name: test\n')
    return {
        'specfile': str(specfile),
        'output': str(tmp_path / 'out.spec'),
        'pkgconfig': False,
        'inline': False,
        'diff': False,
        'diff_prog': 'vimdiff',
        'minimal': False,
        'no_curlification': False,
        'suse_copyright': False,
        'copyright_year': 2013,
        'remove_groups': False,
        'tex': False,
        'perl': False,
        'cmake': False,
        'keep_space': False,
    }


@pytest.fixture
def elements(tmp_path):
    """Build a preamble element handler with the default options."""
    return RpmPreambleElements(RpmSpecCleaner(_default_options(tmp_path)).options)


class TestRpmPreambleElements:
    """We run few tests to ensure the preamble element bookkeeping works fine."""

    def test_sort_helper_key_numbers_unnumbered_source_last(self, elements):
        """Test that the unnumbered Source is sorted as 1, not as 0."""
        assert elements._sort_helper_key('Source: a.tar.gz') == 1
        assert elements._sort_helper_key('Source1: b.tar.gz') == 1
        assert elements._sort_helper_key('Source2: b.tar.gz') == 2

    def test_is_own_lang_package(self, elements):
        """Test that only the -lang subpackage of the main package is recognized."""
        elements.lang_package = {'%{name}-lang'}
        assert elements._is_own_lang_package('%{name}-lang', None) is True
        assert elements._is_own_lang_package('%name-lang', None) is True
        assert elements._is_own_lang_package('other-lang', 'foo') is False
        assert elements._is_own_lang_package('foo', 'foo') is False

    def test_verify_prereq_message_without_prereq(self, elements):
        """Test that the fixme comment is not added when no prereq is present."""
        line = ['BuildRequires: gcc', '']
        assert elements._verify_prereq_message(line) == line
