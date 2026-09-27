#!/usr/bin/env python

import locale

import pytest

from spec_cleaner import RpmExceptionError
from spec_cleaner.fileutils import open_datafile, open_stringio_spec


@pytest.fixture
def c_locale():
    """Switch the process to the C locale so the default encoding is not UTF-8."""
    saved = locale.setlocale(locale.LC_CTYPE)
    locale.setlocale(locale.LC_CTYPE, 'C')
    try:
        if locale.getencoding().lower().replace('-', '') in ('utf8', 'cp65001'):
            pytest.skip('the process runs in UTF-8 mode, the C locale default is not ASCII')
        yield
    finally:
        locale.setlocale(locale.LC_CTYPE, saved)


def _write_datadir(home, name, content):
    """Drop a data file where the home datadir lookup expects it."""
    share = home / '.local' / 'share' / 'spec-cleaner'
    share.mkdir(parents=True, exist_ok=True)
    # bytes, write_text would encode with the ascii default of the C locale
    (share / name).write_bytes(content.encode())
    return share


class TestFileutils:
    """We run few tests to ensure fileutils class works fine."""

    def test_open_assertion(self):
        """Test assert if file can be open with stringio."""
        with pytest.raises(RpmExceptionError, match='missing-file.txt'):
            open_stringio_spec('missing-file.txt')

    def test_open_datafile_assertion(self):
        """Test opening file as datafile."""
        with pytest.raises(RpmExceptionError, match='missing-file.txt'):
            open_datafile('missing-file.txt')

    def test_open(self):
        """Test open and closing file with stringio."""
        data = open_stringio_spec('tests/fileutils-tests.py')
        data.close()

    def test_open_datafile(self):
        """Test open and closing file with datafile."""
        data = open_datafile('excludes-bracketing.txt')
        data.close()

    def test_open_datafile_home_fallback(self, tmp_path, monkeypatch):
        """Test that a data file is found under the home datadir."""
        _write_datadir(tmp_path, 'probe.txt', 'PROBE\n')
        monkeypatch.setenv('HOME', str(tmp_path))
        monkeypatch.delenv('home', raising=False)
        with open_datafile('probe.txt') as data:
            assert data.read() == 'PROBE\n'

    def test_open_datafile_home_unset(self, tmp_path, monkeypatch):
        """Test that a data file is found under ~ when the home is not set."""
        _write_datadir(tmp_path / '~', 'probe.txt', 'PROBE\n')
        monkeypatch.delenv('HOME')
        # the fallback is resolved against the cwd, so the probe has to be there
        monkeypatch.chdir(tmp_path)
        with open_datafile('probe.txt') as data:
            assert data.read() == 'PROBE\n'

    def test_open_stringio_spec_is_utf8(self, tmp_path, c_locale):
        """Test that a spec is read as UTF-8 whatever the locale says."""
        spec = tmp_path / 'utf8.spec'
        spec.write_bytes('Name: café\n'.encode())
        with open_stringio_spec(str(spec)) as data:
            assert data.read() == 'Name: café\n'

    def test_open_datafile_is_utf8(self, tmp_path, monkeypatch, c_locale):
        """Test that a data file is read as UTF-8 whatever the locale says."""
        _write_datadir(tmp_path, 'probe.txt', 'café\n')
        monkeypatch.setenv('HOME', str(tmp_path))
        with open_datafile('probe.txt') as data:
            assert data.read() == 'café\n'
