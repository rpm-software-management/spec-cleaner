#!/usr/bin/env python

import io
import os
import re
import sys

import pytest

from spec_cleaner import RpmExceptionError, RpmSpecCleaner


@pytest.mark.parametrize(
    'diff_prog, expected',
    [
        ('vimdiff', 'vimdiff'),
        ('vimdiff -f', 'vimdiff -f'),
        ('gvimdiff', 'gvimdiff -f'),
        ('gvimdiff -f', 'gvimdiff -f'),
        # the guard looks for a lowercase -f, so an uppercase one still gets one
        ('gvimdiff -F', 'gvimdiff -F -f'),
    ],
)
def test_gvim_diff_prog_is_run_in_the_foreground(default_options, diff_prog, expected):
    """Test that gvim gets a -f so it does not fork, and that nothing else is touched."""
    assert RpmSpecCleaner(default_options(diff_prog=diff_prog)).options['diff_prog'] == expected


def test_diff_argv_is_prog_then_original_then_cleaned(default_options, monkeypatch):
    """Test that the diff program is handed the original spec and the cleaned copy, in that order."""
    options = default_options(output='', diff=True)
    calls = []
    monkeypatch.setattr(
        'spec_cleaner.rpmcleaner.subprocess.call', lambda *a, **kw: calls.append((a, kw))
    )
    cleaner = RpmSpecCleaner(options)
    cleaner.run()
    ((args, kwargs),) = calls
    (cmd,) = args
    assert kwargs == {'shell': False}
    assert cmd == ['vimdiff', options['specfile'], cleaner.fout.name]
    # the diff branch is the only one that builds a named temp file, so the
    # right hand side of the diff is always that file
    assert os.path.isfile(cmd[1])


def test_diff_temp_file_is_named_after_the_spec(default_options):
    """Test that the diff buffer is titled after the spec, not a random temp name."""
    cleaner = RpmSpecCleaner(default_options(output='', diff=True))
    name = os.path.basename(cleaner.fout.name)
    assert re.fullmatch(r'test\.spec\.[a-z0-9_]{8}\.spec', name), name
    assert cleaner.fout.encoding == 'utf-8'


def test_missing_diff_prog_names_the_program(default_options):
    """Test that a diff program which cannot be run is reported by name."""
    options = default_options(output='', diff=True, diff_prog='no-such-diff-program')
    with pytest.raises(RpmExceptionError, match='no-such-diff-program'):
        RpmSpecCleaner(options).run()


def test_stdout_mode_takes_over_stdout_as_utf8(default_options, monkeypatch):
    """Test that with no output target the tool writes to stdout, forced to UTF-8."""
    stream = io.TextIOWrapper(io.BytesIO(), encoding='ascii')
    monkeypatch.setattr(sys, 'stdout', stream)
    cleaner = RpmSpecCleaner(default_options(output=''))
    assert cleaner.fout is stream
    # the spec is UTF-8 whatever the locale charset is
    assert stream.encoding == 'utf-8'


def test_nospeccleaner_is_reported_and_the_spec_copied_verbatim(
    default_options, monkeypatch, capsys
):
    """Test that a skipped spec is copied through untouched and said so on stderr."""
    options = default_options()
    spec = options['specfile']
    with open(spec, 'w', encoding='utf-8') as specfile:
        specfile.write('#nospeccleaner\nName: skipped\n')
    RpmSpecCleaner(options).run()
    # the misspelling of "definition" is the current output, pinned as it stands
    assert capsys.readouterr().err == (
        f".spec file {spec} is not being processed due to definiton of 'nospeccleaner'\n"
    )
    with open(options['output'], encoding='utf-8') as out:
        assert out.read() == '#nospeccleaner\nName: skipped\n'
