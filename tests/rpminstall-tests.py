#!/usr/bin/env python

from collections.abc import Callable
from typing import Any

import pytest

from spec_cleaner.rpmcleaner import RpmSpecCleaner
from spec_cleaner.rpminstall import RpmInstall


@pytest.fixture
def install(default_options: Callable[..., dict[str, Any]]) -> RpmInstall:
    """Build an %install section handler with the default options."""
    return RpmInstall(RpmSpecCleaner(default_options()).options)


class TestRpmInstall:
    """We run few tests to ensure the %install section cleaning works fine."""

    def test_remove_la_keeps_a_foreign_operand(self, install: RpmInstall) -> None:
        """Test that an rm line is not rewritten when a plain operand would be lost."""
        line = 'rm foo %{buildroot}%{_libdir}/*.la'
        assert install._replace_remove_la(line) == line

    def test_clean_drop_keeps_comment_line(self, install: RpmInstall) -> None:
        """A comment mentioning the buildroot cleanup is kept."""
        install.add('# cleanup: rm -rf %{buildroot}')
        assert install.lines == ['# cleanup: rm -rf %{buildroot}']

    def test_clean_drop_removes_real_command(self, install: RpmInstall) -> None:
        """A real buildroot wipe is still dropped."""
        install.add('rm -rf %{buildroot}')
        assert install.lines == []

    def test_remove_la_rewrites_a_la_only_line(self, install: RpmInstall) -> None:
        """Test that an rm line with nothing but .la globs becomes the canonical find."""
        assert (
            install._replace_remove_la('rm -f %{buildroot}%{_libdir}/*.la')
            == 'find %{buildroot} -type f -name "*.la" -delete -print'
        )
