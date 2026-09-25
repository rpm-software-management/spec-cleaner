#!/usr/bin/env python

import pytest

from spec_cleaner.dependency_parser import DependencyParser, DepParserError


class TestDependencyParser:
    """We run few tests to ensure the dependency parser handles malformed input."""

    @pytest.mark.parametrize('line', ['foo >', 'foo >=', 'foo >,', 'foo >= 1, bar <'])
    def test_operator_without_version(self, line):
        """Test that an operator without a version is an error instead of an endless loop."""
        with pytest.raises(DepParserError):
            DependencyParser(line)

    @pytest.mark.parametrize(
        'line, expected',
        [
            ('foo %{?bar:>= 1}', [('foo %{?bar:>= 1}', None, None)]),
            ('foo, %{?bar:>= 1}', [('foo', None, None), ('%{?bar:>= 1}', None, None)]),
            ('foo ,%{?bar:>= 1}', [('foo', None, None), ('%{?bar:>= 1}', None, None)]),
        ],
    )
    def test_conditional_version(self, line, expected):
        """Test that a conditional version joins the dependency before it, but not across a comma."""
        assert DependencyParser(line).parsed == expected
