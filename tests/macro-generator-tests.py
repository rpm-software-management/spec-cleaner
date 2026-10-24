#!/usr/bin/env python

"""Tests for generate-macro-functions.py: repodata verification, package selection."""

import gzip
import hashlib
import importlib.util
import struct
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATOR = REPO_ROOT / 'generate-macro-functions.py'
REPO = 'file:///fixture/'

PRIMARY_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="http://linux.duke.edu/metadata/common" packages="1">
<package type="rpm">
<name>macropkg</name>
<arch>noarch</arch>
<size package="4242" installed="4242" archive="4242"/>
<location href="macropkg-1.0-1.noarch.rpm"/>
</package>
</metadata>
"""

FILELISTS_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<filelists xmlns="http://linux.duke.edu/metadata/filelists" packages="1">
<package pkgid="00" name="macropkg" arch="noarch">
<version epoch="0" ver="1.0" rel="1"/>
<file>/usr/lib/rpm/macros.d/macros.fixture</file>
</package>
</filelists>
"""

MACRO_FILE = '/usr/lib/rpm/macros.d/macros.fixture'


def _load_generator():
    spec = importlib.util.spec_from_file_location('generate_macro_functions', GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _repomd(primary, filelists, algo='sha512', with_checksum=True):
    """Build repomd.xml announcing the given archive bytes."""

    def data(dtype, blob, href):
        checksum = ''
        if with_checksum:
            digest = hashlib.new(algo, blob).hexdigest()
            checksum = f'<checksum type="{algo}">{digest}</checksum>'
        return (
            f'<data type="{dtype}">{checksum}<size>{len(blob)}</size>'
            f'<location href="repodata/{href}"/><timestamp>0</timestamp></data>'
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<repomd xmlns="http://linux.duke.edu/metadata/repo">\n'
        '<revision>12345</revision>\n'
        + data('primary', primary, 'primary.xml.gz')
        + data('filelists', filelists, 'filelists.xml.gz')
        + '</repomd>\n'
    ).encode()


def _stage(
    tmp_path, primary, filelists, announced_primary=None, announced_filelists=None, **kwargs
):
    """
    Stage a workdir the generator's fetch cache serves from.

    The staged archives are what the generator reads; repomd.xml announces
    the announced_* archives, which default to the staged ones.
    """
    gen = _load_generator()
    workdir = tmp_path / 'workdir'
    workdir.mkdir()
    repomd = _repomd(
        announced_primary if announced_primary is not None else primary,
        announced_filelists if announced_filelists is not None else filelists,
        **kwargs,
    )
    (workdir / 'repomd.xml').write_bytes(repomd)
    (workdir / 'primary.xml.gz').write_bytes(primary)
    (workdir / 'filelists.xml.gz').write_bytes(filelists)
    return gen, str(workdir)


def test_verified_archives_parse(tmp_path, capsys):
    """Archives matching their repomd.xml records verify and parse normally."""
    gen, workdir = _stage(tmp_path, gzip.compress(PRIMARY_XML), gzip.compress(FILELISTS_XML))
    hrefs, checks, revision = gen.repodata_hrefs(REPO, workdir)
    assert revision == '12345'
    owners = gen.macro_packages(REPO, workdir, hrefs, checks)
    assert owners == {('macropkg', 'noarch'): [MACRO_FILE]}
    locations = gen.package_locations(REPO, workdir, hrefs, checks)
    assert locations == {('macropkg', 'noarch'): ('macropkg-1.0-1.noarch.rpm', 4242)}
    assert 'Verified' in capsys.readouterr().err


def test_truncated_archive_aborts(tmp_path, capsys):
    """An archive cut short still decompresses cleanly but must abort the run."""
    full = gzip.compress(PRIMARY_XML) + gzip.compress(b'<!-- filler -->')
    truncated = gzip.compress(PRIMARY_XML)
    # The premise: the truncated archive decompresses without any error
    # and even parses into the complete document.
    assert gzip.decompress(truncated) == PRIMARY_XML
    gen, workdir = _stage(tmp_path, truncated, gzip.compress(FILELISTS_XML), announced_primary=full)
    hrefs, checks, _revision = gen.repodata_hrefs(REPO, workdir)
    with pytest.raises(SystemExit):
        gen.package_locations(REPO, workdir, hrefs, checks)
    assert 'Size mismatch' in capsys.readouterr().err


def test_same_size_corruption_aborts(tmp_path, capsys):
    """An archive of the announced size with altered bytes fails the checksum."""
    good = gzip.compress(FILELISTS_XML)
    corrupted = bytearray(good)
    corrupted[len(corrupted) // 2] ^= 0xFF
    gen, workdir = _stage(
        tmp_path, gzip.compress(PRIMARY_XML), bytes(corrupted), announced_filelists=good
    )
    hrefs, checks, _revision = gen.repodata_hrefs(REPO, workdir)
    with pytest.raises(SystemExit):
        gen.macro_packages(REPO, workdir, hrefs, checks)
    assert 'Checksum mismatch' in capsys.readouterr().err


def test_missing_checksum_aborts(tmp_path, capsys):
    """repomd.xml publishing no checksum for a dataset aborts instead of trusting it."""
    gen, workdir = _stage(
        tmp_path,
        gzip.compress(PRIMARY_XML),
        gzip.compress(FILELISTS_XML),
        with_checksum=False,
    )
    hrefs, checks, _revision = gen.repodata_hrefs(REPO, workdir)
    with pytest.raises(SystemExit):
        gen.macro_packages(REPO, workdir, hrefs, checks)
    assert 'no sha256/sha512 checksum' in capsys.readouterr().err


def test_sha256_checksum_accepted(tmp_path):
    """A sha256 record verifies when repomd.xml publishes no sha512."""
    gen, workdir = _stage(
        tmp_path, gzip.compress(PRIMARY_XML), gzip.compress(FILELISTS_XML), algo='sha256'
    )
    hrefs, checks, _revision = gen.repodata_hrefs(REPO, workdir)
    assert checks['primary'][0] == 'sha256'
    owners = gen.macro_packages(REPO, workdir, hrefs, checks)
    assert owners == {('macropkg', 'noarch'): [MACRO_FILE]}


def _cpio_entry(name, body):
    """Build one newc cpio entry holding the given file body."""
    fields = [0, 0o100644, 0, 0, 1, 0, len(body), 0, 0, 0, 0, len(name) + 1, 0]
    out = b'070701' + ''.join(f'{field:08x}' for field in fields).encode()
    out += name.encode() + b'\0'
    out += b'\0' * (-len(out) % 4)
    out += body
    out += b'\0' * (-len(body) % 4)
    return out


def _rpm_bytes(files):
    """Build a minimal rpm holding the given {path: body} payload files."""
    header = b'\x8e\xad\xe8\x01' + b'\0' * 4 + struct.pack('>II', 0, 0)
    payload = b''.join(_cpio_entry('./' + path, body) for path, body in sorted(files.items()))
    payload += _cpio_entry('TRAILER!!!', b'')
    return b'\xed\xab\xee\xdb' + b'\0' * 92 + header + header + payload


SELECTION_PACKAGES = [
    # (name, arch, macro path, macro defined there)
    ('alpha', 'noarch', '/usr/lib/rpm/macros.d/macros.shared', 'shared_alpha'),
    ('beta', 'noarch', '/usr/lib/rpm/macros.d/macros.shared', 'shared_beta'),
    ('delta', 'noarch', '/usr/lib/rpm/macros.d/macros.shared', 'shared_alpha'),
    ('gamma', 'x86_64', '/usr/lib/rpm/macros.d/macros.gamma', 'gamma_x86'),
    ('gamma', 'i686', '/usr/lib/rpm/macros.d/macros.gamma', 'gamma_i686'),
]


def _selection_repodata():
    """Build primary/filelists blobs describing the selection fixture packages."""
    primary_pkgs = []
    filelists_pkgs = []
    for name, arch, path, _macro in SELECTION_PACKAGES:
        href = f'{name}-1.0-1.{arch}.rpm'
        primary_pkgs.append(
            f'<package type="rpm"><name>{name}</name><arch>{arch}</arch>'
            f'<size package="1" installed="1" archive="1"/>'
            f'<location href="{href}"/></package>'
        )
        filelists_pkgs.append(
            f'<package pkgid="00" name="{name}" arch="{arch}">'
            f'<version epoch="0" ver="1.0" rel="1"/><file>{path}</file></package>'
        )
    primary = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<metadata xmlns="http://linux.duke.edu/metadata/common" '
        f'packages="{len(primary_pkgs)}">' + ''.join(primary_pkgs) + '</metadata>\n'
    ).encode()
    filelists = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<filelists xmlns="http://linux.duke.edu/metadata/filelists" '
        f'packages="{len(filelists_pkgs)}">' + ''.join(filelists_pkgs) + '</filelists>\n'
    ).encode()
    return primary, filelists


def _stage_selection(tmp_path):
    """Stage the selection fixture: repodata plus the rpm payloads in the fetch cache."""
    primary, filelists = _selection_repodata()
    gen, workdir = _stage(tmp_path, gzip.compress(primary), gzip.compress(filelists))
    rpms = Path(workdir) / 'rpms'
    rpms.mkdir()
    for name, arch, path, macro in SELECTION_PACKAGES:
        body = f'%{macro}(x) body\n'.encode()
        (rpms / f'{name}-1.0-1.{arch}.rpm').write_bytes(_rpm_bytes({path.lstrip('/'): body}))
    return gen, workdir


def test_every_macro_package_contributes(tmp_path):
    """All filelists owners are read: same-path rivals and arch variants alike."""
    gen, workdir = _stage_selection(tmp_path)
    names, revision, binaries, files_seen = gen.repo_macro_names(REPO, workdir)
    assert revision == '12345'
    # alpha and beta ship macros.shared with different contents; gamma's
    # two arch variants define different macros: all of them contribute.
    assert names == {'shared_alpha', 'shared_beta', 'gamma_x86', 'gamma_i686'}
    assert binaries == 5
    # delta's copy of macros.shared is byte-identical to alpha's: parsed once.
    assert files_seen == 4


def test_owner_without_location_is_skipped_with_a_warning(tmp_path, capsys):
    """A filelists owner the primary data does not locate is reported, not read."""
    gen = _load_generator()
    owners = {('ghost', 'noarch'): [MACRO_FILE]}
    assert gen.all_binaries(owners, {}) == []
    assert 'ghost' in capsys.readouterr().err
