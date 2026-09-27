#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpminstall import RpmInstall


@pytest.fixture
def install(default_options):
    """Build an %install section handler with the default options."""
    return RpmInstall(RpmSpecCleaner(default_options()).options)


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
