#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmpreambleelements import RpmPreambleElements


@pytest.fixture
def elements(default_options):
    """Build a preamble element handler with the default options."""
    return RpmPreambleElements(RpmSpecCleaner(default_options()).options)


class TestRpmPreambleElements:
    """We run few tests to ensure the preamble element bookkeeping works fine."""

    def test_sort_helper_key_numbers_unnumbered_source_last(self, elements):
        """Test that the unnumbered Source is sorted as 1, not as 0."""
        assert elements._sort_helper_key('Source: a.tar.gz') == 1
        assert elements._sort_helper_key('Source1: b.tar.gz') == 1
        assert elements._sort_helper_key('Source2: b.tar.gz') == 2

    def test_is_own_lang_package(self, elements):
        """Test that only the -lang subpackage of the main package is recognized."""
        elements.lang_package = {'%{name}-lang'}
        assert elements._is_own_lang_package('%{name}-lang', None) is True
        assert elements._is_own_lang_package('%name-lang', None) is True
        assert elements._is_own_lang_package('other-lang', 'foo') is False
        assert elements._is_own_lang_package('foo', 'foo') is False

    def test_remove_duplicates_plain_lines(self, elements):
        """Test that identical plain lines deduplicate and merge comments."""
        lines = [
            '#!BuildIgnore:  foo [i586]',
            '#!BuildIgnore:  foo [i586]',
            ['# first note', '#!BuildConflicts: dup [i586]'],
            ['# second note', '#!BuildConflicts: dup [i586]'],
            '#!BuildConflicts: dup >= 1.0 [i586]',
            '#!BuildConflicts: dup [x86_64]',
        ]
        assert elements._remove_duplicates(lines) == [
            '#!BuildIgnore:  foo [i586]',
            ['# first note', '# second note', '#!BuildConflicts: dup [i586]'],
            '#!BuildConflicts: dup >= 1.0 [i586]',
            '#!BuildConflicts: dup [x86_64]',
        ]

    def test_verify_prereq_message_without_prereq(self, elements):
        """Test that the fixme comment is not added when no prereq is present."""
        assert elements._verify_prereq_message(['BuildRequires: gcc', '']) == [
            'BuildRequires: gcc',
            '',
        ]


class TestRpmPreambleElementsOrder:
    """We run few tests to ensure the source position recording works fine."""

    @pytest.fixture
    def elements(self, default_options):
        """Build a preamble element handler with the default options."""
        return RpmPreambleElements(RpmSpecCleaner(default_options()).options)

    @pytest.fixture
    def minimal_elements(self, default_options):
        """Build a preamble element handler with minimal mode options."""
        return RpmPreambleElements(RpmSpecCleaner(default_options(minimal=True)).options)

    def test_positions_recorded_only_in_minimal(self, elements, minimal_elements):
        """Test that positions are recorded in minimal mode only."""
        elements.items['misc'].append('Misc: full')
        assert elements._positions == {}
        minimal_elements.items['name'].append('Name:           test')
        minimal_elements.items['misc'].append('Misc: minimal')
        # moving an element to another bucket keeps its first position
        minimal_elements.items['tail'] += minimal_elements.items['name']
        assert minimal_elements._element_position('Name:           test') == 0
        assert minimal_elements._element_position('Misc: minimal') == 1
        # inserting into a bucket records the position as well
        minimal_elements.items['misc'].insert(0, 'Misc: inserted')
        assert minimal_elements._element_position('Misc: inserted') == 2

    def test_element_position_of_rebuilt_group(self, minimal_elements):
        """Test that a group rebuilt from recorded members resolves to them."""
        group = ['# note', 'Requires:       something']
        minimal_elements.items['requires'].append(group)
        rebuilt = ['# note', '# other note', 'Requires:       something']
        assert minimal_elements._element_position(rebuilt) == 0
        assert minimal_elements._element_position('Requires:       unknown') is None

    def test_flatten_in_source_order_with_unrecorded(self, minimal_elements):
        """Test that an unrecorded element inherits the previous position."""
        minimal_elements.items['name'].append('Name:           test')
        minimal_elements.items['misc'].append('Misc: one')
        minimal_elements.items['misc'].append('Misc: two')
        # simulate an element whose recording was lost: it is emitted
        # right after the element gathered before it
        lost = minimal_elements.items['misc'][0]
        del minimal_elements._positions[id(lost)]
        assert minimal_elements.flatten_output() == [
            'Name:           test',
            'Misc: one',
            'Misc: two',
        ]
