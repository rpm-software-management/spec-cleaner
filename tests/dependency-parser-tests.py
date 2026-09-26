#!/usr/bin/env python

import pytest

from spec_cleaner.dependency_parser import DependencyParser, DepParserError


class TestDependencyParser:
    """We run few tests to ensure the dependency parser handles malformed input."""

    @pytest.mark.parametrize(
        'line, message',
        [
            ('foo >', '^Unexpected end of dependency string'),
            ('foo >=', '^Unexpected end of dependency string'),
            ('foo >,', '^Unexpected end of dependency string'),
            ('foo >= 1, bar <', '^Unexpected end of dependency string'),
        ],
    )
    def test_operator_without_version(self, line, message):
        """Test that an operator without a version is an error instead of an endless loop."""
        with pytest.raises(DepParserError, match=message):
            DependencyParser(line)

    @pytest.mark.parametrize(
        'line, message',
        [
            ('foo >= < 1', '^found operator after operator'),
            ('foo >=1<2', '^found operator after version'),
            ('>= 1', '^found operator when name expected'),
            ('foo >= 1 < 2', '^found operator where a name is expected'),
            ('foo >= 1, < 2', '^found operator where a name is expected'),
        ],
    )
    def test_operator_where_name_or_version_expected(self, line, message):
        """Test that an operator in a place rpm would reject is an error, not a nameless token."""
        with pytest.raises(DepParserError, match=message):
            DependencyParser(line)

    @pytest.mark.parametrize(
        'line, expected',
        [
            ('foo %{?bar:>= 1}', [('foo %{?bar:>= 1}', None, None)]),
            ('foo %{?!bar:>= 1}', [('foo %{?!bar:>= 1}', None, None)]),
            ('foo %{??bar:>= 1}', [('foo %{??bar:>= 1}', None, None)]),
            ('foo %{?bar:>=1}', [('foo %{?bar:>=1}', None, None)]),
            ('foo, %{?bar:>= 1}', [('foo', None, None), ('%{?bar:>= 1}', None, None)]),
            ('foo ,%{?bar:>= 1}', [('foo', None, None), ('%{?bar:>= 1}', None, None)]),
        ],
    )
    def test_conditional_version(self, line, expected):
        """Test that a conditional version joins the dependency before it, but not across a comma."""
        assert DependencyParser(line).parsed == expected

    def test_escaped_percent_stays_in_token(self):
        """Test that a literal %% is not mistaken for the start of a macro."""
        assert DependencyParser('a%%b').parsed == [('a%%b', None, None)]
