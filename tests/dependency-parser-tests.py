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

    @pytest.mark.parametrize(
        'line, macros, expected',
        [
            # a second invocation starts a new dependency instead of becoming
            # an argument of the first one
            (
                '%selfconflict a %selfconflict b',
                ['selfconflict'],
                [('%selfconflict a', None, None), ('%selfconflict b', None, None)],
            ),
            # the second invocation may name a different macro
            (
                '%selfconflict a %other b',
                ['selfconflict', 'other'],
                [('%selfconflict a', None, None), ('%other b', None, None)],
            ),
            # a trailing invocation without arguments still stands on its own
            (
                '%selfconflict a %selfconflict',
                ['selfconflict'],
                [('%selfconflict a', None, None), ('%selfconflict', None, None)],
            ),
            # a version relation after the second invocation belongs to it
            (
                '%selfconflict a %selfconflict b >= 2.0',
                ['selfconflict'],
                [('%selfconflict a', None, None), ('%selfconflict b', '>=', '2.0')],
            ),
            # a braced macro is complete in itself, so as an argument it is
            # part of the invocation before it, never a new invocation
            (
                '%selfconflict %{python_module foo}',
                ['selfconflict', 'python_module'],
                [('%selfconflict %{python_module foo}', None, None)],
            ),
            # an unbraced macro that takes no arguments stays an argument
            (
                '%selfconflict %otherlib liba',
                ['selfconflict'],
                [('%selfconflict %otherlib liba', None, None)],
            ),
        ],
    )
    def test_consecutive_macro_with_arguments(self, line, macros, expected):
        """Test that consecutive invocations split, while arguments stay with their invocation."""
        assert DependencyParser(line, macros_with_arg=macros).parsed == expected

    def test_braced_macro_with_arguments(self):
        """Test that a braced macro invocation is one dependency with no name list."""
        assert DependencyParser('%{python_module foo}').parsed == [
            ('%{python_module foo}', None, None)
        ]

    @pytest.mark.parametrize(
        'line, macros, expected',
        [
            # the libyal BuildRequires lines of gh#492: the argument is part
            # of the invocation, not a dependency of its own
            (
                '%python_module devel',
                ['python_module'],
                [('%python_module devel', None, None)],
            ),
            # a version relation after the argument belongs to the invocation
            (
                '%python_module setuptools >= 40.8.0',
                ['python_module'],
                [('%python_module setuptools', '>=', '40.8.0')],
            ),
            (
                '%python_module Cython >= 0.29',
                ['python_module'],
                [('%python_module Cython', '>=', '0.29')],
            ),
            # a plain macro that takes no arguments is a dependency of its
            # own, and the word after it is the next dependency
            (
                '%plainmacro devel',
                ['python_module'],
                [('%plainmacro', None, None), ('devel', None, None)],
            ),
            # without the macro in the set the invocation splits, which is
            # why the set has to learn it from the rpm macro files
            (
                '%python_module devel',
                [],
                [('%python_module', None, None), ('devel', None, None)],
            ),
        ],
    )
    def test_unbraced_macro_with_arguments(self, line, macros, expected):
        """Test that an unbraced invocation stays one dependency when the macro takes arguments."""
        assert DependencyParser(line, macros_with_arg=macros).parsed == expected

    @pytest.mark.parametrize(
        'line, macros, expected',
        [
            # the braced spelling of an invocation: the braces delimit
            # the name, the arguments still follow it
            (
                '%{python_module} devel',
                ['python_module'],
                [('%{python_module} devel', None, None)],
            ),
            (
                '%{python_module} setuptools >= 40.8.0',
                ['python_module'],
                [('%{python_module} setuptools', '>=', '40.8.0')],
            ),
            # a version relation after a braced use belongs to the
            # dependency, it is not an argument of the macro (gh#500)
            (
                '%{typelib} = %{version}',
                ['typelib'],
                [('%{typelib}', '=', '%{version}')],
            ),
            # without the macro in the set the braced form is a plain
            # name again and the word after it a dependency of its own
            (
                '%{python_module} devel',
                [],
                [('%{python_module}', None, None), ('devel', None, None)],
            ),
        ],
    )
    def test_braced_spelling_macro_with_arguments(self, line, macros, expected):
        """Test that the braced spelling of an invocation parses like the unbraced one."""
        assert DependencyParser(line, macros_with_arg=macros).parsed == expected
