#!/usr/bin/env python

import locale
import os

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
        # the lookup reads HOME, so a lowercase home must not stand in for it
        monkeypatch.delenv('home', raising=False)
        with open_datafile('probe.txt') as data:
            assert data.read() == 'PROBE\n'

    def test_open_datafile_home_unset_uses_the_passwd_entry(self, tmp_path, monkeypatch):
        """Test that an unset home falls back to the passwd entry, not to a ./~ path."""
        # the cwd is not a data source, a ~ directory there must stay unread
        _write_datadir(tmp_path / '~', 'probe.txt', 'CWD\n')
        monkeypatch.delenv('HOME')
        monkeypatch.chdir(tmp_path)
        with pytest.raises(RpmExceptionError):
            open_datafile('probe.txt')
        # and the passwd entry is what the fallback has to end up using
        home = tmp_path / 'home'
        _write_datadir(home, 'probe.txt', 'PROBE\n')
        monkeypatch.setattr(os.path, 'expanduser', lambda path: str(home))
        with open_datafile('probe.txt') as data:
            assert data.read() == 'PROBE\n'

    def test_open_datafile_skips_a_file_that_fails_to_read(self, tmp_path, monkeypatch):
        """Test that a file which opens but then fails to read is closed and skipped."""
        closed = []

        class Unreadable:
            """A file that opens fine and then fails, like a filesystem error mid-read."""

            def read(self):
                """Fail the way an I/O error does."""
                raise OSError(5, 'Input/output error')

            def close(self):
                """Record the close the caller owes us."""
                closed.append(True)

        monkeypatch.setattr('builtins.open', lambda *a, **kw: Unreadable())
        with pytest.raises(RpmExceptionError, match='probe.txt'):
            open_datafile('probe.txt')
        # every candidate path was tried, and each handle was closed
        assert closed

    def test_open_datafile_reports_a_decoding_error(self, tmp_path, monkeypatch):
        """Test that a data file which is not UTF-8 is reported, not read into a UnicodeDecodeError."""
        share = tmp_path / '.local' / 'share' / 'spec-cleaner'
        share.mkdir(parents=True)
        (share / 'probe.txt').write_bytes(b'keyword\ncaf\xe9\n')
        monkeypatch.setenv('HOME', str(tmp_path))
        with pytest.raises(RpmExceptionError, match='probe.txt'):
            open_datafile('probe.txt')

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
