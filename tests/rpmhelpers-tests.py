#!/usr/bin/env python

from io import StringIO
from pathlib import Path
from typing import IO

import pytest

from spec_cleaner import rpmhelpers
from spec_cleaner.fileutils import open_datafile
from spec_cleaner.rpmexception import RpmExceptionError
from spec_cleaner.rpmhelpers import GroupItem
from spec_cleaner.rpmrequirestoken import RpmRequiresToken


class TestRpmhelpers:
    """We run few tests to ensure rpmhelpers functions work fine."""

    def test_load_macro_functions_reads_the_snapshot(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that the vendored snapshot yields its names, headers skipped."""
        rpmhelpers.clear_read_caches()
        content = (
            '# Argument-taking rpm macros from a snapshot\n'
            '# rpm builtins (read from RPM version 4.20.1)\n'
            '\n'
            'autosetup\n'
            'lang_package\n'
            'gsub\n'
        )
        monkeypatch.setattr(rpmhelpers, 'open_datafile', lambda name: StringIO(content))
        assert rpmhelpers.load_macro_functions() == ['autosetup', 'lang_package', 'gsub']
        # the mocked result is cached under the real file's identity and
        # cleaner constructions in other tests do not clear the cache
        rpmhelpers.clear_read_caches()

    def test_load_keywords_whitelist_skips_comments_and_blanks(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that the bracketing excludes loader skips comment and empty lines."""
        rpmhelpers.clear_read_caches()
        content = '# rpm section keyword\nbuild\n\n# %files directive\nattr(\\s*\\([^)]*\\))?\n'
        monkeypatch.setattr(rpmhelpers, 'open_datafile', lambda name: StringIO(content))
        assert rpmhelpers.load_keywords_whitelist() == ['build', 'attr(\\s*\\([^)]*\\))?']
        rpmhelpers.clear_read_caches()

    def test_find_bracketing_macrofuncs_collects_body_arg_defines(self, tmp_path: Path) -> None:
        """Test that defines whose body uses the argument vector are collected for bracketing."""
        spec = tmp_path / 'test.spec'
        spec.write_text(
            '%define declared() %1\n'
            '%define wrapper %{__install} %*\n'
            '%define continued first \\\n'
            '    second %2\n'
            '%define plain plainvalue\n'
            '%global flagonly %{?flag}\n'
            '%define helper %{-c:%{-c*}}\n'
            '%define luapat %{lua: print(("%1"):gsub("%2", "x"))}\n'
        )
        assert rpmhelpers.find_bracketing_macrofuncs(str(spec)) == [
            'declared',
            'wrapper',
            'continued',
        ]

    def test_find_macros_with_arg_keeps_declared_only(self, tmp_path: Path) -> None:
        """Test that the dependency parser's collection stays declaration-based."""
        spec = tmp_path / 'test.spec'
        spec.write_text('%define declared() %1\n%define wrapper %{__install} %*\n')
        assert rpmhelpers.find_macros_with_arg(str(spec)) == ['declared']

    def test_find_bracketing_macrofuncs_trailing_backslash(self, tmp_path: Path) -> None:
        """Test that a definition ending the file mid-continuation does not overrun."""
        spec = tmp_path / 'test.spec'
        spec.write_text('%define dangling body %1 \\\n')
        assert rpmhelpers.find_bracketing_macrofuncs(str(spec)) == ['dangling']

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
    def test_open_macro_bodies(
        self, line: str, depth: tuple[int, int], expected: tuple[int, int]
    ) -> None:
        """Test counting the %{ and %( bodies left open, as rpm does when joining lines."""
        assert rpmhelpers.open_macro_bodies(line, depth) == expected

    def test_fix_license_keeps_a_name_ending_in_x(self) -> None:
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
    def test_fix_license_rewrites_the_suffix(self, value: str, expected: str) -> None:
        """Test that the two non-SPDX suffixes rpm accepts are spelled out."""
        assert rpmhelpers.fix_license(value, rpmhelpers.read_licenses_changes()) == expected

    def test_fix_license_empty_value(self) -> None:
        """Test that an empty license stays empty instead of joining a None."""
        assert rpmhelpers.fix_license('', {}) == ''

    @pytest.mark.parametrize('value', [';MIT', ' ; MIT', 'MIT; ', ';MIT;', 'MIT;'])
    def test_fix_license_drops_a_separator_without_an_operand(self, value: str) -> None:
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
    def test_conversion_tables_are_well_formed(self, name: str) -> None:
        """Test that every line of a generated table still carries the separator."""
        with open_datafile(name) as data:
            for number, line in enumerate(data, 1):
                assert ': ' in line, f'{name} line {number}: {line!r}'

    def test_table_reads_are_replayed_not_reread(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that a parsed table is reused instead of read and parsed again."""
        rpmhelpers.clear_read_caches()
        real_open = open_datafile
        calls: list[str] = []

        def counting(name: str) -> IO[str]:
            calls.append(name)
            return real_open(name)

        monkeypatch.setattr(rpmhelpers, 'open_datafile', counting)
        first = rpmhelpers.read_licenses_changes()
        second = rpmhelpers.read_licenses_changes()
        assert first == second
        assert first is not second
        assert calls == [rpmhelpers.LICENSES_CHANGES]

    def test_read_conversion_changes_reports_a_malformed_line(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that a line without the separator is reported instead of unpacked."""
        rpmhelpers.clear_read_caches()
        monkeypatch.setattr(
            rpmhelpers, 'open_datafile', lambda name: StringIO('good: a b \nbroken\n')
        )
        with pytest.raises(RpmExceptionError, match='Line 2'):
            rpmhelpers.read_conversion_changes('probe_conversions.txt')

    def test_add_group_names_the_type_it_cannot_flatten(self) -> None:
        """Test that the guard reports the offending type."""
        with pytest.raises(RpmExceptionError, match="<class 'int'>"):
            rpmhelpers.add_group(42)  # type: ignore[arg-type]  # int on purpose: the guard has to name it

    def test_read_licenses_changes_keeps_a_key_ending_in_x(self) -> None:
        """Test that reading the table does not trim a trailing letter off a key."""
        rpmhelpers.clear_read_caches()
        conversions = rpmhelpers.read_licenses_changes()
        assert conversions['SUSE-TeX'] == 'SUSE-TeX'
        assert 'SUSE-Te' not in conversions

    def test_read_licenses_changes_keeps_the_first_row(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that no leading row is silently dropped as a presumed header."""
        rpmhelpers.clear_read_caches()
        monkeypatch.setattr(
            rpmhelpers, 'open_datafile', lambda name: StringIO('0BSD\t0BSD\nMIT\tMIT\n')
        )
        assert rpmhelpers.read_licenses_changes() == {'0BSD': '0BSD', 'MIT': 'MIT'}

    def test_read_licenses_changes_skips_comment_lines(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that the provenance header is not parsed as a mapping row."""
        rpmhelpers.clear_read_caches()
        monkeypatch.setattr(
            rpmhelpers,
            'open_datafile',
            lambda name: StringIO(
                '# SPDX license list 3.29.0, fetched 2026-09-28\n0BSD\t0BSD\nMIT\tMIT\n'
            ),
        )
        assert rpmhelpers.read_licenses_changes() == {'0BSD': '0BSD', 'MIT': 'MIT'}

    def test_fix_license_passes_a_known_zero_clause_through(self) -> None:
        """Test that the shortest real id survives, now via the table itself."""
        rpmhelpers.clear_read_caches()
        assert rpmhelpers.fix_license('0BSD', rpmhelpers.read_licenses_changes()) == '0BSD'

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
    def test_find_pkgconfig_declaration(self, name: str, declaration: bool) -> None:
        """Test that a pkgconfig build dependency is spotted, bracketed or not."""
        elements = [RpmRequiresToken(name, None, None, 'BuildRequires:')]
        assert rpmhelpers.find_pkgconfig_declaration(elements) is declaration

    def test_sort_uniq_merges_duplicate_sources(self) -> None:
        """Test that duplicates merge and no following line is dropped."""
        source = 'Source:         %{name}-%{version}.tar.gz'
        extra = 'Source1:        extra.tar.gz'
        # a plain duplicate that is not the last item
        assert rpmhelpers.sort_uniq([source, source, extra]) == [source, extra]
        # a duplicate whose comments merge, also not the last item
        merged: list[GroupItem] = ['# one', '# two', source]
        assert rpmhelpers.sort_uniq([['# one', source], ['# two', source], extra]) == [
            merged,
            extra,
        ]
        # a plain duplicate of an already commented group
        assert rpmhelpers.sort_uniq([merged, source, extra]) == [merged, extra]
