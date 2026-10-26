#!/usr/bin/env python

from collections.abc import Callable
from typing import Any

import pytest

from spec_cleaner.rpmcleaner import RpmSpecCleaner
from spec_cleaner.rpmhelpers import GroupItem
from spec_cleaner.rpmpreambleelements import RpmPreambleElements


@pytest.fixture
def elements(default_options: Callable[..., dict[str, Any]]) -> RpmPreambleElements:
    """Build a preamble element handler with the default options."""
    return RpmPreambleElements(RpmSpecCleaner(default_options()).options)


class TestRpmPreambleElements:
    """We run few tests to ensure the preamble element bookkeeping works fine."""

    def test_sort_helper_key_numbers_unnumbered_source_last(
        self, elements: RpmPreambleElements
    ) -> None:
        """Test that the unnumbered Source is sorted as 1, not as 0."""
        assert elements._sort_helper_key('Source: a.tar.gz') == 1
        assert elements._sort_helper_key('Source1: b.tar.gz') == 1
        assert elements._sort_helper_key('Source2: b.tar.gz') == 2

    def test_is_own_lang_package(self, elements: RpmPreambleElements) -> None:
        """Test that only the -lang subpackage of the main package is recognized."""
        elements.lang_package = {'%{name}-lang'}
        assert elements._is_own_lang_package('%{name}-lang', None) is True
        assert elements._is_own_lang_package('%name-lang', None) is True
        assert elements._is_own_lang_package('other-lang', 'foo') is False
        assert elements._is_own_lang_package('foo', 'foo') is False

    def test_remove_duplicates_plain_lines(self, elements: RpmPreambleElements) -> None:
        """Test that identical plain lines deduplicate and merge comments."""
        lines: list[GroupItem] = [
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

    def test_verify_prereq_message_without_prereq(self, elements: RpmPreambleElements) -> None:
        """Test that the fixme comment is not added when no prereq is present."""
        assert elements._verify_prereq_message(['BuildRequires: gcc', '']) == [
            'BuildRequires: gcc',
            '',
        ]


class TestRpmPreambleElementsOrder:
    """We run few tests to ensure the source position recording works fine."""

    @pytest.fixture
    def elements(self, default_options: Callable[..., dict[str, Any]]) -> RpmPreambleElements:
        """Build a preamble element handler with the default options."""
        return RpmPreambleElements(RpmSpecCleaner(default_options()).options)

    @pytest.fixture
    def minimal_elements(
        self, default_options: Callable[..., dict[str, Any]]
    ) -> RpmPreambleElements:
        """Build a preamble element handler with minimal mode options."""
        return RpmPreambleElements(RpmSpecCleaner(default_options(minimal=True)).options)

    def test_positions_recorded_only_in_minimal(
        self, elements: RpmPreambleElements, minimal_elements: RpmPreambleElements
    ) -> None:
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

    def test_element_position_of_rebuilt_group(self, minimal_elements: RpmPreambleElements) -> None:
        """Test that a group rebuilt from recorded members resolves to them."""
        group: list[GroupItem] = ['# note', 'Requires:       something']
        minimal_elements.items['requires'].append(group)
        rebuilt: list[GroupItem] = ['# note', '# other note', 'Requires:       something']
        assert minimal_elements._element_position(rebuilt) == 0
        assert minimal_elements._element_position('Requires:       unknown') is None

    def test_rebuilt_group_assigned_to_bucket_resolves_through_members(
        self, minimal_elements: RpmPreambleElements
    ) -> None:
        """Test that a rebuilt group assigned to a bucket gets no own position."""
        group: list[GroupItem] = ['# note', 'Requires:       something']
        minimal_elements.items['requires'].append(group)
        minimal_elements.items['requires'].append('Requires:       other')
        rebuilt: list[GroupItem] = ['# note', '# other note', 'Requires:       something']
        minimal_elements.items['misc'] = [rebuilt]
        assert minimal_elements._element_position(rebuilt) == 0
        assert minimal_elements._element_position('Requires:       other') == 1

    def test_has_recorded_member_through_nested_list(
        self, minimal_elements: RpmPreambleElements
    ) -> None:
        """Test that a rebuilt group is detected through a member in a nested list."""
        recorded = 'Requires:       recorded'
        minimal_elements.items['requires'].append(recorded)
        nested: list[GroupItem] = ['Requires:       inner', recorded]
        rebuilt: list[GroupItem] = ['Requires:       outer', nested]
        # the recorded member is found only by descending into the nested list
        assert minimal_elements._has_recorded_member(rebuilt) is True
        # so the rebuilt group gets no own position and resolves through it,
        # and the element gathered after it takes the next position
        minimal_elements.items['misc'] = [rebuilt]
        following = 'Misc:           following'
        minimal_elements.items['misc'].append(following)
        assert minimal_elements._element_position(rebuilt) == 0
        assert minimal_elements._element_position(following) == 1

    def test_has_recorded_member_with_only_unrecorded_nested_members(
        self, minimal_elements: RpmPreambleElements
    ) -> None:
        """Test that a group with nothing recorded in its nested list is recorded itself."""
        nested: list[GroupItem] = ['Requires:       inner one', 'Requires:       inner two']
        group: list[GroupItem] = ['Requires:       outer', nested]
        # the walk descends into the nested list and still finds nothing
        assert minimal_elements._has_recorded_member(group) is False
        # so the group is recorded with its own position, nested list included
        minimal_elements.items['misc'] = [group]
        following = 'Misc:           following'
        minimal_elements.items['misc'].append(following)
        assert minimal_elements._element_position(group) == 0
        assert minimal_elements._element_position(nested) == 0
        assert minimal_elements._element_position(following) == 1

    def test_flatten_after_duplicate_absorb_keeps_source_order(
        self, minimal_elements: RpmPreambleElements
    ) -> None:
        """Test that a group absorbing a duplicate's comments stays in place."""
        line = "BuildRequires:  %(rpm -q --queryformat '%{VERSION}' dup)"
        minimal_elements.items['buildrequires'].append(['# first comment', line])
        minimal_elements.items['buildrequires'].append([line])
        minimal_elements.items['requires'].append('Requires:       zzz-last')
        assert minimal_elements.flatten_output() == [
            '# first comment',
            line,
            'Requires:       zzz-last',
        ]

    def test_flatten_after_repeated_duplicate_absorbs_keeps_source_order(
        self, minimal_elements: RpmPreambleElements
    ) -> None:
        """Test that repeated absorbs of one line keep its first position."""
        line = "BuildRequires:  %(rpm -q --queryformat '%{VERSION}' dup)"
        minimal_elements.items['buildrequires'].append(['# first comment', line])
        minimal_elements.items['buildrequires'].append(['# second comment', line])
        minimal_elements.items['buildrequires'].append([line])
        minimal_elements.items['requires'].append('Requires:       zzz-last')
        assert minimal_elements.flatten_output() == [
            '# first comment',
            '# second comment',
            line,
            'Requires:       zzz-last',
        ]

    def test_flatten_after_duplicate_without_comments_keeps_source_order(
        self, minimal_elements: RpmPreambleElements
    ) -> None:
        """Test that duplicates without comments to merge stay in place."""
        line = "BuildRequires:  %(rpm -q --queryformat '%{VERSION}' dup)"
        minimal_elements.items['buildrequires'].append([line])
        minimal_elements.items['buildrequires'].append([line])
        minimal_elements.items['requires'].append('Requires:       zzz-last')
        assert minimal_elements.flatten_output() == [
            line,
            'Requires:       zzz-last',
        ]

    def test_flatten_in_source_order_with_unrecorded(
        self, minimal_elements: RpmPreambleElements
    ) -> None:
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
