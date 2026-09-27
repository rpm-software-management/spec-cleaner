#!/usr/bin/env python

import pytest

from spec_cleaner import RpmExceptionError, rpmhelpers


class TestRpmhelpers:
    """We run few tests to ensure rpmhelpers functions work fine."""

    def test_parse_rpm_showrc_locale_charset(self, monkeypatch):
        """Test parsing 'rpm --showrc' output printed in a non-UTF-8 locale (cs_CZ)."""
        output = b'-13: __apply_patch(qp:m:)\t\n==== aktivn\xed 1073 pr\xe1zdn\xe9 0\n'
        monkeypatch.setattr(rpmhelpers, 'check_output', lambda cmd: output)
        assert rpmhelpers.parse_rpm_showrc() == ['__apply_patch']

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
