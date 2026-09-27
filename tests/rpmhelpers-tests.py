#!/usr/bin/env python

from io import StringIO

import pytest

from spec_cleaner import RpmExceptionError, rpmhelpers
from spec_cleaner.fileutils import open_datafile
from spec_cleaner.rpmrequirestoken import RpmRequiresToken


class TestRpmhelpers:
    """We run few tests to ensure rpmhelpers functions work fine."""

    def test_parse_rpm_showrc_locale_charset(self, monkeypatch):
        """Test parsing 'rpm --showrc' output printed in a non-UTF-8 locale (cs_CZ)."""
        output = (
            b'-13: __apply_patch(qp:m:)\t\n'
            b'-14: __os_install_post(qp:m:)\t\n'
            b'-15: foo(bar)\t\n'
            b'==== aktivn\xed 1073 pr\xe1zdn\xe9 0\n'
        )
        monkeypatch.setattr(rpmhelpers, 'check_output', lambda cmd: output)
        assert rpmhelpers.parse_rpm_showrc() == ['__apply_patch', '__os_install_post', 'foo']

    def test_parse_rpm_showrc_missing_rpm(self, monkeypatch):
        """Test that a missing rpm binary is reported as RpmExceptionError."""

        def missing(cmd):
            raise FileNotFoundError(2, 'No such file or directory', 'rpm')

        monkeypatch.setattr(rpmhelpers, 'check_output', missing)
        with pytest.raises(RpmExceptionError):
            rpmhelpers.parse_rpm_showrc()

    @pytest.mark.parametrize(
        'line, depth, expected',
        [
            ('%define a %{lua:', (0, 0), (1, 0)),
            ('%global b %(echo 1 |', (0, 0), (0, 1)),
            ('%global c %{expand:%{x}', (0, 0), (1, 0)),
            ('%define d %{x} {', (0, 0), (0, 0)),
            ('%define e %%{x} \\%{y', (0, 0), (0, 0)),
            ('if x then print("{") end', (1, 0), (2, 0)),
            ('}', (1, 0), (0, 0)),
            ('tr 1 2)', (0, 1), (0, 0)),
            # the char behind a backslash is skipped, so its %{ opens nothing
            ('\\%{', (1, 0), (2, 0)),
            # %% is an escaped percent, it never opens a body
            ('%%{', (0, 0), (0, 0)),
            # a %{ pair opens once, the brace is consumed with the percent
            ('%%{', (1, 0), (2, 0)),
            # every %( on the line adds up, the counter is not just set
            ('%(a | %(b |', (0, 0), (0, 2)),
            # only braces move the brace counter; the X is here because it is the
            # one character a mutation of the '{}' set would add
            ('%{lua:print("X")}', (1, 0), (1, 0)),
            # ...and likewise the paren counter
            ('%(echo "X" |', (0, 1), (0, 2)),
            # a ( inside an open %( body counts, balanced within it or not
            ("%(rpm -q x | cut -d'(' -f2)", (0, 0), (0, 1)),
        ],
    )
    def test_open_macro_bodies(self, line, depth, expected):
        """Test counting the %{ and %( bodies left open, as rpm does when joining lines."""
        assert rpmhelpers.open_macro_bodies(line, depth) == expected

    def test_fix_license_keeps_a_name_ending_in_x(self):
        """Test that trimming the trailing semicolon does not eat a trailing letter."""
        conversions = rpmhelpers.read_licenses_changes()
        assert conversions['SUSE-TeX'] == 'SUSE-TeX'
        assert rpmhelpers.fix_license('SUSE-TeX', conversions) == 'SUSE-TeX'

    @pytest.mark.parametrize(
        'value, expected',
        [
            ('MIT-ORlater', 'MIT-or later'),
            ('MIT-ORsim', 'MIT-or similar'),
        ],
    )
    def test_fix_license_rewrites_the_suffix(self, value, expected):
        """Test that the two non-SPDX suffixes rpm accepts are spelled out."""
        assert rpmhelpers.fix_license(value, rpmhelpers.read_licenses_changes()) == expected

    def test_fix_license_empty_value(self):
        """Test that an empty license stays empty instead of joining a None."""
        assert rpmhelpers.fix_license('', {}) == ''

    @pytest.mark.parametrize('value', [';MIT', ' ; MIT', 'MIT; ', ';MIT;', 'MIT;'])
    def test_fix_license_drops_a_separator_without_an_operand(self, value):
        """Test that a separator missing an operand is dropped, not turned into a dangling AND."""
        assert rpmhelpers.fix_license(value, {}) == 'MIT'

    @pytest.mark.parametrize(
        'name',
        [
            rpmhelpers.TEX_CONVERSIONS,
            rpmhelpers.PKGCONFIG_CONVERSIONS,
            rpmhelpers.CMAKE_CONVERSIONS,
            rpmhelpers.PERL_CONVERSIONS,
        ],
    )
    def test_conversion_tables_are_well_formed(self, name):
        """Test that every line of a generated table still carries the separator."""
        with open_datafile(name) as data:
            for number, line in enumerate(data, 1):
                assert ': ' in line, f'{name} line {number}: {line!r}'

    def test_read_conversion_changes_reports_a_malformed_line(self, monkeypatch):
        """Test that a line without the separator is reported instead of unpacked."""
        monkeypatch.setattr(
            rpmhelpers, 'open_datafile', lambda name: StringIO('good: a b \nbroken\n')
        )
        with pytest.raises(RpmExceptionError, match='Line 2'):
            rpmhelpers.read_conversion_changes('probe_conversions.txt')

    def test_add_group_names_the_type_it_cannot_flatten(self):
        """Test that the guard reports the offending type."""
        with pytest.raises(RpmExceptionError, match="<class 'int'>"):
            rpmhelpers.add_group(42)

    def test_read_licenses_changes_keeps_a_key_ending_in_x(self):
        """Test that reading the table does not trim a trailing letter off a key."""
        conversions = rpmhelpers.read_licenses_changes()
        assert conversions['SUSE-TeX'] == 'SUSE-TeX'
        assert 'SUSE-Te' not in conversions

    @pytest.mark.parametrize(
        'name, declaration',
        [
            ('pkgconfig', True),
            ('pkgconfig(fftw3)', False),
            ('pkgconfig %{?v:>= 1}', True),
            ('%{?with_x}pkgconfig', True),
            ('pkgconfig-x11', False),
        ],
    )
    def test_find_pkgconfig_declaration(self, name, declaration):
        """Test that a pkgconfig build dependency is spotted, bracketed or not."""
        elements = [RpmRequiresToken(name, None, None, 'BuildRequires:')]
        assert rpmhelpers.find_pkgconfig_declaration(elements) is declaration

    def test_sort_uniq_merges_duplicate_sources(self):
        """Test that duplicates merge and no following line is dropped."""
        source = 'Source:         %{name}-%{version}.tar.gz'
        extra = 'Source1:        extra.tar.gz'
        # a plain duplicate that is not the last item
        assert rpmhelpers.sort_uniq([source, source, extra]) == [source, extra]
        # a duplicate whose comments merge, also not the last item
        merged = ['# one', '# two', source]
        assert rpmhelpers.sort_uniq([['# one', source], ['# two', source], extra]) == [
            merged,
            extra,
        ]
        # a plain duplicate of an already commented group
        assert rpmhelpers.sort_uniq([merged, source, extra]) == [merged, extra]
