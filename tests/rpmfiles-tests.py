#!/usr/bin/env python

from collections.abc import Callable
from typing import Any

import pytest

from spec_cleaner.rpmcleaner import RpmSpecCleaner
from spec_cleaner.rpmfiles import RpmFiles


@pytest.fixture
def files(default_options: Callable[..., dict[str, Any]]) -> RpmFiles:
    """Build an %files section handler with the default options."""
    return RpmFiles(RpmSpecCleaner(default_options()).options)


@pytest.fixture
def files_minimal(default_options: Callable[..., dict[str, Any]]) -> RpmFiles:
    """Build an %files section handler running in minimal mode."""
    return RpmFiles(RpmSpecCleaner(default_options(minimal=True)).options)


class TestRpmFiles:
    """We run few tests to ensure the %files section cleaning works fine."""

    def test_strip_useless_spaces(self, files: RpmFiles) -> None:
        """Test that the aligned %files entries get their interior padding squeezed out."""
        files.add('%doc /a  b')
        assert files.lines == ['%doc /a b']

    def test_python_sitelib_without_specfile(self, files: RpmFiles) -> None:
        """Test that the module name falls back to the macro when the spec file name is not known."""
        files.spec = ''
        assert files._expand_python_sitelib('%{python_sitelib}/*') == (
            '%{python_sitelib}/%{name}\n%{python_sitelib}/%{name}-%{version}*-info'
        )

    def test_remove_doc_on_man_only_pages(self) -> None:
        """Test that a line listing only man/info pages loses its %doc prefix."""
        assert RpmFiles._remove_doc_on_man('%doc %{_mandir}/man1/foo.1%{ext_man}') == (
            '%{_mandir}/man1/foo.1%{ext_man}'
        )
        assert RpmFiles._remove_doc_on_man(
            '%doc %{_infodir}/foo.info.gz %{_mandir}/man1/foo.1'
        ) == ('%{_infodir}/foo.info.gz %{_mandir}/man1/foo.1')

    def test_remove_doc_on_man_mixed_line(self) -> None:
        """Test that a line mixing man pages with other files keeps its %doc prefix."""
        line = '%doc %{_mandir}/man1/foo.1%{ext_man} README'
        assert RpmFiles._remove_doc_on_man(line) == line

    def test_minimal_keeps_doc_on_man(self, files_minimal: RpmFiles) -> None:
        """Test that minimal mode keeps the %doc prefix on man pages."""
        files_minimal.add('%doc %{_mandir}/man1/foo.1%{ext_man}')
        assert files_minimal.lines == ['%doc %{_mandir}/man1/foo.1%{ext_man}']

    def test_minimal_keeps_doc_license(self, files_minimal: RpmFiles) -> None:
        """Test that minimal mode does not move licence files from %doc to %license."""
        files_minimal.add('%doc COPYING README')
        assert files_minimal.lines == ['%doc COPYING README']
