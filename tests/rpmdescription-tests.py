#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmdescription import RpmDescription


@pytest.fixture
def description(default_options):
    """Build a %description section handler with the default options."""
    return RpmDescription(RpmSpecCleaner(default_options()).options)


class TestRpmDescription:
    """We run few tests to ensure the %description section cleaning works fine."""

    def test_authors_block_after_text_keeps_the_blank_line(self, description):
        """Test that a dropped Authors block only eats the blank line it introduced."""
        for line in ('%description', 'Text here', 'Authors: x', ''):
            description.add(line)
        assert description.lines == ['%description', 'Text here', '']

    def test_single_character_line_before_a_blank_line(self, description):
        """Test that a blank line after a one character line is still kept."""
        for line in ('%description', 'q', ''):
            description.add(line)
        assert description.lines == ['%description', 'q', '']

    def test_bare_percent_stops_losing_track_of_the_section(self, description):
        """Test that a lone % is still read as a macro use, so the Authors block stays."""
        for line in ('%description', '%', 'Authors: x', ''):
            description.add(line)
        assert description.lines == ['%description', '%', 'Authors: x', '']
