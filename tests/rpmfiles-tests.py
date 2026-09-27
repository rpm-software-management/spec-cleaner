#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmfiles import RpmFiles


@pytest.fixture
def files(default_options):
    """Build an %files section handler with the default options."""
    return RpmFiles(RpmSpecCleaner(default_options()).options)


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
