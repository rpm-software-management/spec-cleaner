#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmfiles import RpmFiles


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
def files(tmp_path):
    return RpmFiles(RpmSpecCleaner(_default_options(tmp_path)).options)


class TestRpmFiles:
    """We run few tests to ensure the %files section cleaning works fine."""

    def test_strip_useless_spaces(self, files):
        """Test that the aligned %files entries get their interior padding squeezed out."""
        files.add('%doc /a  b')
        assert files.lines == ['%doc /a b']

    def test_python_sitelib_without_specfile(self, files):
        """Test that the module name falls back to the macro when the spec file name is not known."""
        files.spec = ''
        assert files._expand_python_sitelib('%{python_sitelib}/*') == (
            '%{python_sitelib}/%{name}\n%{python_sitelib}/%{name}-%{version}*-info'
        )
