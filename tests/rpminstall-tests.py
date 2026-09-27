#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpminstall import RpmInstall


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
def install(tmp_path):
    """Build an %install section handler with the default options."""
    return RpmInstall(RpmSpecCleaner(_default_options(tmp_path)).options)


class TestRpmInstall:
    """We run few tests to ensure the %install section cleaning works fine."""

    def test_remove_la_keeps_a_foreign_operand(self, install):
        """Test that an rm line is not rewritten when a plain operand would be lost."""
        line = 'rm foo %{buildroot}%{_libdir}/*.la'
        assert install._replace_remove_la(line) == line

    def test_remove_la_rewrites_a_la_only_line(self, install):
        """Test that an rm line with nothing but .la globs becomes the canonical find."""
        assert (
            install._replace_remove_la('rm -f %{buildroot}%{_libdir}/*.la')
            == 'find %{buildroot} -type f -name "*.la" -delete -print'
        )
