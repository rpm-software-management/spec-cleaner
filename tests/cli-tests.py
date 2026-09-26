#!/usr/bin/env python

import os
import re
import sys
from datetime import datetime

import pytest

from spec_cleaner import __version__, main, process_args
from spec_cleaner.rpmexception import RpmWrongArgsError

SPEC = """\
Name:           cli-test
Version:        1.0
Release:        0
Summary:        Test package
License:        MIT
URL:            https://example.org/cli-test

%description
Test package.

%changelog
"""


@pytest.fixture
def specfile(tmp_path):
    """Write a minimal spec file and hand back its path."""
    path = tmp_path / 'cli-test.spec'
    path.write_text(SPEC)
    return path


def test_missing_spec_is_refused(capsys, tmp_path):
    """Test that a nonexistent spec is refused with a message and a failing exit code."""
    missing = tmp_path / 'nope.spec'
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sys, 'argv', ['spec-cleaner', str(missing)])
        assert main() == 1
    assert capsys.readouterr().err == f'ERROR: {missing} does not exist.\n'


def test_clean_run_exits_zero(capsys, monkeypatch, specfile, tmp_path):
    """Test that a successful run reports success and writes the output file."""
    out = tmp_path / 'out.spec'
    monkeypatch.setattr(sys, 'argv', ['spec-cleaner', '-o', str(out), str(specfile)])
    assert main() == 0
    assert capsys.readouterr().err == ''
    assert out.read_text().startswith('Name:           cli-test')


def test_output_must_not_be_overwritten(tmp_path, specfile):
    """Test that an existing output file is only replaced with --force."""
    out = tmp_path / 'out.spec'
    out.write_text('untouched\n')
    with pytest.raises(RpmWrongArgsError, match='already exists.'):
        process_args([str(specfile), '-o', str(out)])
    assert process_args([str(specfile), '-o', str(out), '--force'])['force'] is True


def test_output_path_is_expanded(tmp_path, specfile):
    """Test that a ~ in the output path is expanded before the file is looked up."""
    options = process_args([str(specfile), '-o', '~/cli-test-out.spec'])
    assert options['output'] == os.path.expanduser('~/cli-test-out.spec')
    assert not options['output'].startswith('~')


@pytest.mark.parametrize('argv', [['-d', '-o', 'out'], ['-i', '-o', 'out']])
def test_output_modes_are_exclusive(argv, specfile):
    """Test that diff and inline cannot be combined with an output file."""
    with pytest.raises(SystemExit):
        process_args([str(specfile), *argv])


def test_no_arguments_prints_help(capsys):
    """Test that an empty argument list prints the help and exits successfully."""
    with pytest.raises(SystemExit) as exit_info:
        process_args([])
    assert exit_info.value.code == 0
    assert '--pkgconfig' in capsys.readouterr().out


def test_version_exits_successfully(capsys, specfile):
    """Test that --version prints the package version and exits successfully."""
    with pytest.raises(SystemExit) as exit_info:
        process_args(['--version', str(specfile)])
    assert exit_info.value.code == 0
    printed = capsys.readouterr().out.strip()
    # compared against the module attribute, not a literal, so bumping the
    # release does not break the suite; the format is still pinned
    assert printed == __version__
    assert re.fullmatch(r'\d+\.\d+\.\d+', printed)


def test_copyright_year_must_be_a_number(specfile):
    """Test that a non-numeric copyright year is rejected by the parser."""
    with pytest.raises(SystemExit):
        process_args([str(specfile), '--copyright-year', 'notayear'])


def test_defaults(capsys, specfile):
    """Test the defaults that the rest of the tool is built on."""
    options = process_args([str(specfile)])
    assert options['copyright_year'] == datetime.now().year
    assert options['diff_prog'] == 'vimdiff'
    assert options['output'] == ''
    with pytest.raises(SystemExit):
        process_args(['--help', str(specfile)])
    assert '(default:' in capsys.readouterr().out
