"""
Shared test fixtures.

The acceptance and CLI tests run the full cleaner, whose macro
knowledge comes from the vendored snapshot and from the spec under
test, so the suite runs on machines without the rpm binary.
"""

import pytest


@pytest.fixture
def default_options(tmp_path):
    """
    Build the options dict the section tests hand to RpmSpecCleaner.

    Returns a builder taking keyword overrides. The dict is built fresh per
    test, so a test may mutate what it gets back.
    """
    specfile = tmp_path / 'test.spec'
    specfile.write_text('Name: test\n')
    defaults = {
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
    return lambda **overrides: {**defaults, **overrides}
