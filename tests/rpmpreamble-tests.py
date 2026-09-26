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
