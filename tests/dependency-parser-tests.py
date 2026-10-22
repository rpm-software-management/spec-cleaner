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
            ('foo %{!?bar:>= 1}', [('foo %{!?bar:>= 1}', None, None)]),
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

    @pytest.mark.parametrize(
        'line, expected',
        [
            # the gcc shape: the invocation and its argument are one dependency
            (
                '%selfconflict libgcc_s%{libgcc_s}',
                [('%selfconflict libgcc_s%{libgcc_s}', None, None)],
            ),
            (
                '%selfconflict libgcc_s%{libgcc_s}-32bit',
                [('%selfconflict libgcc_s%{libgcc_s}-32bit', None, None)],
            ),
            # the invocation takes a whole argument list
            ('%selfconflict liba libb', [('%selfconflict liba libb', None, None)]),
            # an invocation in the middle of the line, ending it
            (
                'foo %selfconflict bar',
                [('foo', None, None), ('%selfconflict bar', None, None)],
            ),
            # a comma ends the invocation and starts the next dependency
            (
                '%selfconflict liba, %selfconflict libb',
                [('%selfconflict liba', None, None), ('%selfconflict libb', None, None)],
            ),
            (
                '%selfconflict bar, foo',
                [('%selfconflict bar', None, None), ('foo', None, None)],
            ),
            # an operator ends the invocation: the relation belongs to the
            # dependency the invocation expands to
            ('%selfconflict bar >= 1.0', [('%selfconflict bar', '>=', '1.0')]),
            # an invocation without arguments stays a single dependency
            ('%selfconflict', [('%selfconflict', None, None)]),
            # a macro that is not known to take arguments still splits
            ('%otherlib liba', [('%otherlib', None, None), ('liba', None, None)]),
        ],
    )
    def test_macro_with_arguments(self, line, expected):
        """Test that an invocation of a macro that takes arguments stays one dependency."""
        assert DependencyParser(line, macros_with_arg=['selfconflict']).parsed == expected

    def test_braced_macro_with_arguments(self):
        """Test that a braced macro invocation is one dependency with no name list."""
        assert DependencyParser('%{python_module foo}').parsed == [
            ('%{python_module foo}', None, None)
        ]
