#!/usr/bin/env python

import pytest

from spec_cleaner import RpmSpecCleaner
from spec_cleaner.rpmdescription import RpmDescription


def _default_options(tmp_path):
    """Create the default options dict for tests."""
    specfile = tmp_path / 'test.spec'
    specfile.write_text('Name: test\n')
    return {
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


@pytest.fixture
def description(tmp_path):
    """Build a %description section handler with the default options."""
    return RpmDescription(RpmSpecCleaner(_default_options(tmp_path)).options)


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
