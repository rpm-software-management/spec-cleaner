#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmhelpers import add_group
from spec_cleaner.rpmpreamble import RpmPreamble


def kinds(line):
    """Spell the tags of the line: g for global, c for condition, e for eager."""
    tags = (('g', 'is_global'), ('c', 'is_cond'), ('e', 'is_eager'))
    return ''.join(tag for tag, attr in tags if getattr(line, attr, False))


class TestRpmPreamble:
    """We run few tests to ensure the preamble records the define units while parsing."""

    @pytest.fixture
    def preamble(self, tmp_path):
        """Create a preamble section with the options of a default run."""
        specfile = tmp_path / 'test.spec'
        specfile.write_text('Name: test\n')
        options = {
            'specfile': str(specfile),
            'output': str(tmp_path / 'out.spec'),
            'pkgconfig': False,
            'inline': False,
            'diff': False,
            'diff_prog': 'vimdiff',
            'minimal': False,
            'no_curlification': False,
            'suse_copyright': False,
            'copyright_year': 2013,
            'remove_groups': False,
            'tex': False,
            'perl': False,
            'cmake': False,
            'keep_space': False,
        }
        return RpmPreamble(RpmSpecCleaner(options).options)

    @pytest.fixture
    def minimal_preamble(self, tmp_path):
        """Create a preamble section with the options of a minimal run."""
        specfile = tmp_path / 'test.spec'
        specfile.write_text('Name: test\n')
        options = {
            'specfile': str(specfile),
            'output': str(tmp_path / 'out.spec'),
            'pkgconfig': False,
            'inline': False,
            'diff': False,
            'diff_prog': 'vimdiff',
            'minimal': True,
            'no_curlification': False,
            'suse_copyright': False,
            'copyright_year': 2013,
            'remove_groups': False,
            'tex': False,
            'perl': False,
            'cmake': False,
            'keep_space': False,
        }
        return RpmPreamble(RpmSpecCleaner(options).options)

    @staticmethod
    def units(preamble, *lines):
        """Add the lines and list the define units as (line, tags) pairs."""
        for line in lines:
            preamble.add(line)
        return [
            [(str(line), kinds(line)) for line in add_group(unit)]
            for unit in preamble.paragraph.items['define']
        ]

    def test_single_lines(self, preamble):
        """Test that each define line is a unit and only a %global is expanded when parsed."""
        assert self.units(preamble, '%define a 1', '# b', '%global b 2') == [
            [('%define a 1', '')],
            [('# b', ''), ('%global b 2', 'ge')],
        ]

    def test_multiline_macros(self, preamble):
        """Test that a multiline macro is one unit tagged as its first line."""
        lines = (
            '%global a \\',
            'x \\',
            'y',
            '%define b \\',
            'z',
            '%global c %{expand:',
            '%{x}',
            '}',
        )
        assert self.units(preamble, *lines, '%global d %{expand:%{x}}') == [
            [('%global a \\', 'ge'), ('x \\', 'ge'), ('y', 'ge')],
            [('%define b \\', ''), ('z', '')],
            [('%global c %{expand:', 'ge'), ('%{x}', 'ge'), ('}', 'ge')],
            [('%global d %{expand:%{x}}', 'ge')],
        ]

    def test_open_macro_bodies(self, preamble):
        """Test that a macro continues while a lua or shell body is open, as rpm joins the lines."""
        lines = ('%define a %{lua:', 'print("{}")', '}', '%global b %(echo 1 |', 'tr 1 2)')
        assert self.units(preamble, *lines, '%define c 1') == [
            [('%define a %{lua:', ''), ('print("{}")', ''), ('}', '')],
            [('%global b %(echo 1 |', 'ge'), ('tr 1 2)', 'ge')],
            [('%define c 1', '')],
        ]

    def test_oneline_conditions(self, preamble):
        """Test that a one-line condition is expanded when parsed, even around %define."""
        assert self.units(preamble, '%{?with_a:%define a 1}', '%{?with_b:%global b 1}') == [
            [('%{?with_a:%define a 1}', 'e')],
            [('%{?with_b:%global b 1}', 'ge')],
        ]

    def test_condition_block(self, preamble):
        """Test that a %if block is one unit, continued conditions included."""
        lines = ('%if 0%{?a} || \\', '0%{?b}', '%define x 1', '%elif 0%{?c} || \\', '0%{?d}')
        assert self.units(preamble, *lines, '%define x 2', '%endif') == [
            [
                ('%if 0%{?a} || \\', 'ce'),
                ('0%{?b}', 'ce'),
                ('%define x 1', ''),
                ('%elif 0%{?c} || \\', 'ce'),
                ('0%{?d}', 'ce'),
                ('%define x 2', ''),
                ('%endif', ''),
            ]
        ]

    def test_multiline_condition_block(self, preamble):
        """Test that a %{?cond: block is one unit, split at its closing brace."""
        assert self.units(preamble, '%{?with_a:', '%global b 1}') == [
            [('%{?with_a:', 'ce'), ('%global b 1', 'ge'), ('}', '')]
        ]

    def test_nested_block(self, preamble):
        """Test that the lines of a nested block keep their tags in the outer unit."""
        lines = ('%if 0%{?a}', '%if 0%{?b}', '%global c 1', '%endif', '%endif')
        assert self.units(preamble, *lines) == [
            [
                ('%if 0%{?a}', 'ce'),
                ('%if 0%{?b}', 'ce'),
                ('%global c 1', 'ge'),
                ('%endif', ''),
                ('%endif', ''),
            ]
        ]

    def test_block_lines_outside_define(self, preamble):
        """Test that block lines placed outside the defines keep their tags."""
        lines = ('%if 0%{?a}', '%define x 1', '%{?with_b:BuildRequires:  b}')
        assert self.units(preamble, *lines, '%global kernel_module_v 1', '%endif') == [
            [
                ('%if 0%{?a}', 'ce'),
                ('%define x 1', ''),
                ('%global kernel_module_v 1', 'ge'),
                ('%{?with_b:BuildRequires:  b}', 'e'),
                ('%endif', ''),
            ]
        ]

    def test_tail_macro_before_block(self, preamble):
        """Test that a tail macro kept in a block is a unit apart from the nested block after it."""
        lines = ('%if 0%{?a}', '%python_subpackages', '%if 0%{?b}', '%define x 1', '%endif')
        assert self.units(preamble, *lines) == [
            [('%python_subpackages', '')],
            [('%if 0%{?b}', 'ce'), ('%define x 1', ''), ('%endif', '')],
        ]

    def test_pruned_block(self, preamble):
        """Test that a block pruned as empty adds no unit."""
        lines = ('%if 0%{?a}', '%if 0%{?b}', '%define x 1', '%endif', '%else', '%if 0%{?c}')
        assert self.units(preamble, *lines, '%endif') == []

    def test_late_global_units(self, preamble):
        """Test the flags of the units reading the tags or the bconds."""
        lines = (
            '%bcond_with foo',
            '%global v %{version}',
            '%define w %{v}',
            '%global z %{w}',
            '%define v 2',
            '%define lazy %{with foo}',
            '%global eager %{with foo}',
            '%global reader %{lazy}',
        )
        self.units(preamble, *lines)
        paragraph = preamble.paragraph
        flagged = paragraph._late_global_units(paragraph.items['define'], paragraph._bcond_macros())
        assert [(late, after_bconds) for _, late, after_bconds in flagged] == [
            (True, False),
            (False, False),
            (True, False),
            (True, False),
            (False, False),
            (False, True),
            (False, True),
        ]

    def test_late_global_units_conditions(self, preamble):
        """Test that conditions and one-line conditions pass on what they read."""
        lines = (
            '%bcond_with foo',
            '%global v %{version}',
            '%if 0%{?v}',
            '%define a 1',
            '%endif',
            '%{?with_foo:%define d 1}',
        )
        self.units(preamble, *lines)
        paragraph = preamble.paragraph
        flagged = paragraph._late_global_units(paragraph.items['define'], paragraph._bcond_macros())
        assert [(late, after_bconds) for _, late, after_bconds in flagged] == [
            (True, False),
            (True, False),
            (False, True),
        ]

    def test_late_global_units_tail_macro(self, preamble):
        """Test that a unit invoking a section-generating macro is late."""
        lines = (
            '%if %{with python}',
            '%define python_subpackage_only 1',
            '%python_subpackages',
            '%endif',
            '%define plain 1',
        )
        self.units(preamble, *lines)
        paragraph = preamble.paragraph
        flagged = paragraph._late_global_units(paragraph.items['define'], paragraph._bcond_macros())
        assert [(late, after_bconds) for _, late, after_bconds in flagged] == [
            (True, True),
            (False, False),
        ]

    def test_dep_pragma_entries(self, preamble):
        """Test that a dep pragma value splits into entries and marks the qualified ones."""
        split = preamble._split_dep_pragma_entries
        assert split('foo bar >= 1.0') == [('foo', False), ('bar >= 1.0', False)]
        assert split('foo [x86_64], bar') == [('foo [x86_64]', True), ('bar', False)]
        assert split('foo >= 1.0 [home:proj]') == [('foo >= 1.0 [home:proj]', True)]
        assert split('%{base_name}-bootstrap') == [('%{base_name}-bootstrap', False)]
        # rich dependencies and empty values do not split into plain entries
        assert split('(foo or bar)') is None
        assert split('') is None
        # a qualifier cannot lead the entries, and only spaces, tabs and
        # commas separate them: anything else keeps the value unsplit
        assert split('[i586] foo') is None
        assert split('foo\rbar') is None
        assert split('foo\r') is None

    def test_dep_pragma_normalization(self, preamble):
        """Test that dep pragmas convert to the plain tags and qualified entries stay pragmas."""
        preamble.add('#!BuildRequires: foo [x86_64] bar >= 1.0')
        preamble.add('#!BuildConflicts: oldthing')
        preamble.add('#!BuildRequires: (foo or bar)')
        preamble.add('#!BuildRequires: [i586] foo')
        items = preamble.paragraph.items
        assert [str(item) for item in items['buildrequires']] == ['BuildRequires:  bar >= 1.0']
        assert [str(item) for item in items['buildrequires_pragma']] == [
            '#!BuildRequires: foo [x86_64]',
            '#!BuildRequires: (foo or bar)',
            '#!BuildRequires: [i586] foo',
        ]
        assert [str(item) for item in items['buildconflicts']] == ['BuildConflicts: oldthing']
        assert items['buildconflicts_pragma'] == []

    def test_dep_pragma_conditional_entries(self, preamble):
        """Test that entries with conditional macros stay pragmas while plain entries convert."""
        preamble.add('#!BuildRequires: %{?with_x:condpkg}')
        preamble.add('#!BuildRequires: %{!?with_x:condpkg}')
        preamble.add('#!BuildRequires: plainpkg %{?with_y:otherpkg}')
        preamble.add('#!BuildConflicts: %{?with_x:oldpkg}')
        items = preamble.paragraph.items
        assert [str(item) for item in items['buildrequires']] == ['BuildRequires:  plainpkg']
        assert [str(item) for item in items['buildrequires_pragma']] == [
            '#!BuildRequires: %{?with_x:condpkg}',
            '#!BuildRequires: %{!?with_x:condpkg}',
            '#!BuildRequires: %{?with_y:otherpkg}',
        ]
        assert items['buildconflicts'] == []
        assert [str(item) for item in items['buildconflicts_pragma']] == [
            '#!BuildConflicts: %{?with_x:oldpkg}'
        ]

    def test_dep_pragma_unbraced_conditional_entries(self, preamble):
        """Test that entries with unbraced conditional macros stay pragmas."""
        preamble.add('#!BuildRequires: %?foo')
        preamble.add('#!BuildRequires: %!?foo')
        preamble.add('#!BuildRequires: plainpkg %?bar')
        preamble.add('#!BuildConflicts: %?oldpkg')
        items = preamble.paragraph.items
        assert [str(item) for item in items['buildrequires']] == ['BuildRequires:  plainpkg']
        assert [str(item) for item in items['buildrequires_pragma']] == [
            '#!BuildRequires: %?foo',
            '#!BuildRequires: %!?foo',
            '#!BuildRequires: %?bar',
        ]
        assert items['buildconflicts'] == []
        assert [str(item) for item in items['buildconflicts_pragma']] == [
            '#!BuildConflicts: %?oldpkg'
        ]

    def test_dep_pragma_comment_on_both_split_lines(self, preamble):
        """Test that a trailing comment is kept on both lines of a plain+qualified split."""
        preamble.add('#!BuildConflicts: mixold mixq [i586] # legacy combo')
        preamble.add('#!BuildRequires: plainpkg %?bar # needed sometimes')
        items = preamble.paragraph.items
        assert [str(item) for item in items['buildconflicts']] == [
            'BuildConflicts: mixold # legacy combo'
        ]
        assert [str(item) for item in items['buildconflicts_pragma']] == [
            '#!BuildConflicts: mixq [i586] # legacy combo'
        ]
        assert [str(item) for item in items['buildrequires']] == [
            'BuildRequires:  plainpkg # needed sometimes'
        ]
        assert [str(item) for item in items['buildrequires_pragma']] == [
            '#!BuildRequires: %?bar # needed sometimes'
        ]

    def test_dep_pragma_malformed_entries(self, preamble):
        """Test that malformed dep pragma values do not split into tags rpm rejects."""
        split = preamble._split_dep_pragma_entries
        # a version relation after a qualifier is not an entry of its own:
        # brackets and operators cannot start a token
        assert split('foo [x86_64] >= 1.0') is None
        # a bracket glued to the name is the entry's qualifier
        assert split('nospace[x86_64]') == [('nospace[x86_64]', True)]
        preamble.add('#!BuildRequires: foo [x86_64] >= 1.0')
        preamble.add('#!BuildRequires: nospace[x86_64]')
        items = preamble.paragraph.items
        assert items['buildrequires'] == []
        assert [str(item) for item in items['buildrequires_pragma']] == [
            '#!BuildRequires: foo [x86_64] >= 1.0',
            '#!BuildRequires: nospace[x86_64]',
        ]

    def test_pragma_values_kept_whole_in_minimal_mode(self, preamble, minimal_preamble):
        """Test that a minimal run keeps pragma values whole while a full run splits them."""
        fix = minimal_preamble._fix_list_of_packages
        assert fix('foo >= 1.0 bar', 'buildrequires_pragma') == ['foo >= 1.0 bar']
        assert fix('libacl-devel pkg-config', 'buildconflicts_pragma') == [
            'libacl-devel pkg-config'
        ]
        assert fix('zeta alpha beta gamma', 'buildignores') == ['zeta alpha beta gamma']
        # a qualified value stays whole in both modes, so the gate changes nothing there
        assert fix('qualified [i586] other', 'buildrequires_pragma') == ['qualified [i586] other']
        full = preamble._fix_list_of_packages
        assert full('qualified [i586] other', 'buildrequires_pragma') == ['qualified [i586] other']
        tokens = full('foo >= 1.0 bar', 'buildrequires_pragma')
        assert [(token.name, token.operator, token.version) for token in tokens] == [
            ('foo', '>=', '1.0'),
            ('bar', None, None),
        ]
        tokens = full('zeta alpha beta gamma', 'buildignores')
        assert [token.name for token in tokens] == ['zeta', 'alpha', 'beta', 'gamma']

    def test_empty_macros_with_arg(self, preamble):
        """Test that an empty macro set parses an invocation as separate dependencies."""
        options = dict(preamble.options)
        options['macros_with_arg'] = []
        empty = RpmPreamble(options)
        # without a known macro the parser cannot tell the braced form is
        # an invocation, so it and its argument stay separate dependencies
        tokens = empty._fix_list_of_packages('%{python_module} devel', 'buildrequires')
        assert [token.name for token in tokens] == ['%{python_module}', 'devel']
        # with the macro known the parser recognises the invocation in
        # the braced spelling as written, no unbracing needed
        tokens = preamble._fix_list_of_packages('%{python_module} devel', 'buildrequires')
        assert [token.name for token in tokens] == ['%{python_module} devel']
        # a version relation after a braced use is a relation, not an
        # argument of the macro (gh#500)
        tokens = preamble._fix_list_of_packages('%{typelib} = %{version}', 'requires')
        assert [(token.name, token.operator, token.version) for token in tokens] == [
            ('%{typelib}', '=', '%{version}'),
        ]
        # a braced use that closes the value captures nothing and
        # unbraces like any other macro name
        tokens = preamble._fix_list_of_packages('foo >= %{pkg_version}', 'requires')
        assert [(token.name, token.operator, token.version) for token in tokens] == [
            ('foo', '>=', '%pkg_version'),
        ]
        # plain values parse the same with and without the macro set
        for section in (preamble, empty):
            tokens = section._fix_list_of_packages('foo >= 1.0 bar', 'buildrequires')
            assert [(token.name, token.operator, token.version) for token in tokens] == [
                ('foo', '>=', '1.0'),
                ('bar', None, None),
            ]


class TestRpmPreambleOrder:
    """We run few tests to ensure minimal mode keeps the preamble order."""

    @pytest.fixture(params=[False, True], ids=['full', 'minimal'])
    def preamble_mode(self, tmp_path, request):
        """Create a preamble section, in a full and in a minimal run."""
        specfile = tmp_path / 'test.spec'
        specfile.write_text('Name: test\n')
        options = {
            'specfile': str(specfile),
            'output': str(tmp_path / 'out.spec'),
            'pkgconfig': False,
            'inline': False,
            'diff': False,
            'diff_prog': 'vimdiff',
            'minimal': request.param,
            'no_curlification': False,
            'suse_copyright': False,
            'copyright_year': 2013,
            'remove_groups': False,
            'tex': False,
            'perl': False,
            'cmake': False,
            'keep_space': False,
        }
        return RpmPreamble(RpmSpecCleaner(options).options)

    SCRAMBLED = [
        'Requires:       zzz-package',
        '%define mydef 1',
        'Name:           scramble',
        'BuildRequires:  zlib-devel',
        'Version:        1.0',
        'Release:        0',
        'Summary:        Scramble test',
        'License:        MIT',
        '%if %{with foo}',
        '%define incond 1',
        '%endif',
        'Source0:        scramble.tar.gz',
        '%bcond_with foo',
    ]

    @staticmethod
    def _flatten(preamble, lines):
        for line in lines:
            preamble.add(line)
        return preamble.paragraph.flatten_output()

    def test_preserves_source_order(self, preamble_mode):
        """Test that minimal mode emits the preamble in source order."""
        if not preamble_mode.minimal:
            pytest.skip('source order is a minimal mode property')
        assert self._flatten(preamble_mode, self.SCRAMBLED) == self.SCRAMBLED

    def test_full_mode_reorders(self, preamble_mode):
        """Test that a full run still emits the canonical category order."""
        if preamble_mode.minimal:
            pytest.skip('canonical order is a full run property')
        assert self._flatten(preamble_mode, self.SCRAMBLED) == [
            '%define mydef 1',
            '%bcond_with foo',
            '%if %{with foo}',
            '%define incond 1',
            '%endif',
            'Name:           scramble',
            'Version:        1.0',
            'Release:        0',
            'Summary:        Scramble test',
            'License:        MIT',
            'Source0:        scramble.tar.gz',
            'BuildRequires:  zlib-devel',
            'Requires:       zzz-package',
        ]

    def test_minimal_block_below_name_stays(self, preamble_mode):
        """Test that a block defining subpackages stays below the Name tag."""
        if not preamble_mode.minimal:
            pytest.skip('source order is a minimal mode property')
        lines = [
            'Name:           blocktest',
            'Version:        1.0',
            'Release:        0',
            'Summary:        Block test',
            'License:        MIT',
            '%if %{with python}',
            '%define python_subpackage_only 1',
            '%python_subpackages',
            '%endif',
        ]
        assert self._flatten(preamble_mode, lines) == lines
