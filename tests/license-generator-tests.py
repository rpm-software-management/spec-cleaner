#!/usr/bin/env python

"""Tests for generate-licenses-for-rpmlint.py output."""

import subprocess
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATOR = REPO_ROOT / 'generate-licenses-for-rpmlint.py'
EXCEPTIONS = REPO_ROOT / 'spec_cleaner' / 'data' / 'license_exceptions.txt'


def _exception_ids():
    return [
        line.strip()
        for line in EXCEPTIONS.read_text().splitlines()
        if line.strip() and not line.startswith('#')
    ]


def _generate(tmp_path, *extra_args):
    out = tmp_path / 'licenses.toml'
    subprocess.run(
        [sys.executable, str(GENERATOR), *extra_args, str(out)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return tomllib.loads(out.read_text())


def test_exceptions_section_matches_source(tmp_path):
    """The ValidLicenseExceptions section mirrors license_exceptions.txt exactly."""
    data = _generate(tmp_path)
    assert data['ValidLicenseExceptions'] == _exception_ids()


def test_exceptions_section_present_with_suse_flag(tmp_path):
    """The --suse output carries the same exceptions section."""
    data = _generate(tmp_path, '--suse')
    assert data['ValidLicenseExceptions'] == _exception_ids()
    assert data['ValidLicenses'] != _generate(tmp_path)['ValidLicenses']


def test_exceptions_nonempty_and_sorted(tmp_path):
    """Guard against an empty or accidentally reordered exceptions list."""
    exceptions = _generate(tmp_path)['ValidLicenseExceptions']
    assert len(exceptions) > 0
    assert exceptions == sorted(exceptions)


def test_checked_in_tomls_match_generator(tmp_path):
    """The committed TOMLs are exactly what the generator produces (release backstop)."""
    for name in ('licenses.toml', 'licenses-suse.toml'):
        args = ('--suse',) if name == 'licenses-suse.toml' else ()
        generated = _generate(tmp_path, *args)
        committed = tomllib.loads((REPO_ROOT / 'spec_cleaner' / 'data' / name).read_text())
        assert generated == committed, name
