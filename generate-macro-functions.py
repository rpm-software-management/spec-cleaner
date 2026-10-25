#!/usr/bin/env python3
"""
Generate the vendored list of argument-taking rpm macros.

The list is built from the distribution itself, in the same spirit as the
conversion tables: every package in the repository that installs a file
into the rpm macro directories contributes its macro definitions, and a
macro is listed when its definition carries an argument list, or its body
consumes the argument vector (``%1``..``%9``, ``%*``, ``%#``). A ``%{-n}``
style reference in a body is not an argument signal: it reads the option
of the macro whose expansion is in progress, a helper's idiom.

The rpm builtin macros form a separate section of the output.  They are
read from ``rpm --showrc`` on the generation host; builtins change only
with rpm itself, so a refresh may keep the recorded section instead of
re-reading it (``--keep-builtins``), which is what the scheduled sync
does: the runner's rpm there is older than the one the section was
recorded from and its dump does not list every builtin.

Usage:
    generate-macro-functions.py [--repo URL] [--out FILE] [--workdir DIR]
                                [--keep-builtins]

The snapshot unions two rolling development distributions: openSUSE
Tumbleweed, the distribution the Factory corpus is built from, and
Fedora Rawhide, whose macro packages cover the macro vocabulary of the
Fedora ecosystem.  Only python3 and the zstd binary are needed; rpm
payloads are extracted directly, without rpm2cpio/cpio.

Downloaded repodata is verified against the checksum and size published
for it in repomd.xml before it is parsed, the same discipline
conversions-update.sh applies to the conversion tables: an incomplete
or stale download aborts the run instead of producing a silently
shortened macro list. The rpm payloads are verified the same way,
against the checksum and size the primary metadata publishes for each
package, before they are parsed.
"""

import argparse
import bz2
import gzip
import hashlib
import lzma
import os
import re
import struct
import subprocess
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

DEFAULT_REPO = 'https://download.opensuse.org/tumbleweed/repo/oss/'
DEFAULT_FEDORA_REPO = (
    'https://download.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/'
)

NS = {
    'r': 'http://linux.duke.edu/metadata/repo',
    'c': 'http://linux.duke.edu/metadata/common',
    'f': 'http://linux.duke.edu/metadata/filelists',
}
R_TAG = '{' + NS['r'] + '}'
C_TAG = '{' + NS['c'] + '}'
F_TAG = '{' + NS['f'] + '}'

MACRO_PATH = re.compile(r'^/usr/lib/rpm/(?:[^/]+/)*macros(?:\.[^/]*)?$')

# A macro body consumes its arguments when it references the argument
# vector (%1 .. %9, %*, %** or %#).
ARG_REF = re.compile(r'%(?:[1-9#*]|\*\*|\{[1-9#*]\}|\{\*\*?\}|\{\?[*#1-9]|\{#)')

DEF_RE = re.compile(r'^%([A-Za-z_][A-Za-z0-9_]*)(?:\(([^)]*)\))?[ \t]*(.*)$')
DEFINE_RE = re.compile(
    r'^%(?:define|global)[ \t]+([A-Za-z_][A-Za-z0-9_]*)(?:\(([^)]*)\))?[ \t]*(.*)$'
)
BUILTIN_RE = re.compile(r'^-[0-9]+[:=]\s(\w+)[ \t]+<builtin>[ \t]*$')

BUILTINS_MARKER = '# rpm builtins'


def fetch(url, dest):
    """Download a URL to a local path, unless it is already there."""
    if not os.path.exists(dest):
        print(f'fetch {url}', file=sys.stderr)
        urllib.request.urlretrieve(url, dest)
    return dest


def open_metadata(path):
    """Open a downloaded repodata file, whatever its compression."""
    if path.endswith('.zst'):
        proc = subprocess.Popen(['zstd', '-dc', path], stdout=subprocess.PIPE)
        return proc.stdout
    if path.endswith('.gz'):
        return gzip.open(path, 'rb')
    return open(path, 'rb')


def checksum_record(data):
    """Return the (algorithm, checksum, size) repomd.xml publishes for one data element."""
    by_type = {}
    for el in data.findall(R_TAG + 'checksum'):
        if el.text:
            by_type[el.get('type')] = el.text.strip()
    algo = next((a for a in ('sha512', 'sha256') if a in by_type), None)
    size_el = data.find(R_TAG + 'size')
    size = int(size_el.text) if size_el is not None and size_el.text else None
    return algo, by_type.get(algo), size


def _file_digest(path, algo):
    """Return the (hexdigest, size) of a local file under one algorithm."""
    digest = hashlib.new(algo)
    total = 0
    with open(path, 'rb') as fh:
        while chunk := fh.read(1024 * 1024):
            digest.update(chunk)
            total += len(chunk)
    return digest.hexdigest(), total


def verify_archive(path, href, record, repo):
    """
    Verify a downloaded repodata archive against its repomd.xml record.

    The run aborts when repomd.xml publishes no usable checksum, or when
    the download's size or checksum differs from the published one: a
    truncated archive can still decompress cleanly (cut at a frame
    boundary), and a mirror can serve a complete but stale file, so a
    successful decompression alone proves nothing.
    """
    algo, expected, size = record
    if not algo or not expected:
        print(
            f'repomd.xml of "{repo}" publishes no sha256/sha512 checksum for {href}',
            file=sys.stderr,
        )
        sys.exit(1)
    actual, total = _file_digest(path, algo)
    if size is not None and total != size:
        print(
            f'Size mismatch for {href}: repomd.xml announces {size} bytes, got {total}',
            file=sys.stderr,
        )
        sys.exit(1)
    if actual != expected:
        print(
            f'Checksum mismatch for {href}: repomd.xml announces {expected}, got {actual}',
            file=sys.stderr,
        )
        sys.exit(1)
    print(f'Verified {href} against the {algo} checksum in repomd.xml', file=sys.stderr)


def verify_package(path, href, checksum, size):
    """
    Verify a downloaded rpm against the record the primary data publishes.

    The run aborts when the primary data publishes no usable checksum,
    or when the download's size or checksum differs from the published
    one: a corrupt rpm still parses as a cpio stream, with the damaged
    entries silently missing, so a successful parse proves nothing.
    """
    algo, expected = checksum
    if not algo or not expected:
        print(f'primary data publishes no checksum for {href}', file=sys.stderr)
        sys.exit(1)
    actual, total = _file_digest(path, algo)
    if size and total != size:
        print(
            f'Size mismatch for {href}: primary data announces {size} bytes, got {total}',
            file=sys.stderr,
        )
        sys.exit(1)
    if actual != expected:
        print(
            f'Checksum mismatch for {href}: primary data announces {expected}, got {actual}',
            file=sys.stderr,
        )
        sys.exit(1)


def repomd_cache_name(repo):
    """
    Name of the workdir cache file for one repository's repomd.xml.

    The name is keyed to the repository: a workdir reused with another
    --repo value holds each repository's repomd.xml separately, so one
    repository's cached file is never read as another's.
    """
    return 'repomd-' + hashlib.sha256(repo.encode()).hexdigest()[:16] + '.xml'


def repodata_hrefs(repo, workdir):
    """Read repomd.xml; return the data hrefs, their verification records, the revision."""
    repomd = fetch(repo + 'repodata/repomd.xml', os.path.join(workdir, repomd_cache_name(repo)))
    tree = ET.parse(repomd)
    hrefs = {}
    checks = {}
    for data in tree.getroot().iter(R_TAG + 'data'):
        hrefs[data.get('type')] = data.find(R_TAG + 'location').get('href')
        checks[data.get('type')] = checksum_record(data)
    rev_el = tree.getroot().find(R_TAG + 'revision')
    return hrefs, checks, rev_el.text if rev_el is not None else 'unknown'


def macro_packages(repo, workdir, hrefs, checks):
    """Map package identity -> [macro file paths] from the filelists."""
    path = fetch(
        repo + hrefs['filelists'], os.path.join(workdir, os.path.basename(hrefs['filelists']))
    )
    verify_archive(path, hrefs['filelists'], checks.get('filelists', (None, None, None)), repo)
    owners = {}
    with open_metadata(path) as fh:
        pkg = None
        for event, el in ET.iterparse(fh, events=('start', 'end')):
            if el.tag == F_TAG + 'package':
                if event == 'start':
                    pkg = (el.get('name'), el.get('arch'))
                else:
                    pkg = None
                    el.clear()
            elif pkg and event == 'end' and el.tag == F_TAG + 'file':
                if el.text and el.get('type') != 'dir' and MACRO_PATH.match(el.text):
                    owners.setdefault(pkg, []).append(el.text)
                el.clear()
    return owners


def package_locations(repo, workdir, hrefs, checks):
    """Map (name, arch) -> (location href, package size, package checksum) from the primary data."""
    path = fetch(repo + hrefs['primary'], os.path.join(workdir, os.path.basename(hrefs['primary'])))
    verify_archive(path, hrefs['primary'], checks.get('primary', (None, None, None)), repo)
    locations = {}
    with open_metadata(path) as fh:
        cur = None
        for event, el in ET.iterparse(fh, events=('start', 'end')):
            if el.tag == C_TAG + 'package':
                if event == 'start':
                    cur = {}
                else:
                    if cur.get('name') and cur.get('location'):
                        locations[(cur['name'], cur.get('arch'))] = (
                            cur['location'],
                            cur.get('size', 0),
                            cur.get('checksum', (None, None)),
                        )
                    cur = None
                    el.clear()
            elif cur is not None and event == 'end':
                if el.tag == C_TAG + 'name':
                    cur['name'] = el.text
                elif el.tag == C_TAG + 'arch':
                    cur['arch'] = el.text
                elif el.tag == C_TAG + 'location':
                    cur['location'] = el.get('href')
                elif el.tag == C_TAG + 'size':
                    cur['size'] = int(el.get('package', '0'))
                elif el.tag == C_TAG + 'checksum':
                    record = (el.get('type'), (el.text or '').strip())
                    if el.get('pkgid') or 'checksum' not in cur:
                        cur['checksum'] = record
    return locations


def all_binaries(owners, locations):
    """
    Every binary the filelists show installing macro files, in a stable order.

    Coverage is exhaustive by construction: each (name, arch) pair in
    the filelists contributes its macro files. A package is not skipped
    because another package ships a file at the same path — the copies
    do not necessarily agree (cmake and cmake-mini both ship
    macros.cmake, each llvm version ships its own macros.llvm) — and no
    architecture variant stands in for its siblings, whose macro files
    can differ just as well.
    """
    binaries = []
    for (name, arch), files in sorted(owners.items()):
        loc = locations.get((name, arch))
        if loc is None:
            print(
                f'warning: {name} ({arch}) installs macro files but has '
                'no location in the primary data; skipped',
                file=sys.stderr,
            )
            continue
        binaries.append((name, arch, files, loc[0], loc[1], loc[2]))
    return binaries


def _header_end(data, offset):
    """Skip one rpm header starting at offset; return the offset past it."""
    if data[offset : offset + 3] != b'\x8e\xad\xe8':
        raise ValueError('bad rpm header magic')
    nindex, hsize = struct.unpack('>II', data[offset + 8 : offset + 16])
    return offset + 16 + nindex * 16 + hsize


def rpm_payload(data):
    """Return the (decompressed) cpio payload of an rpm package."""
    if data[:4] != b'\xed\xab\xee\xdb':
        raise ValueError('not an rpm package')
    offset = 96  # lead
    offset = _header_end(data, offset)
    offset = (offset + 7) & ~7  # signature header is 8-byte aligned
    offset = _header_end(data, offset)
    payload = data[offset:]
    if payload[:6] == b'\x28\xb5\x2f\xfd\x00\x00' or payload[:4] == b'\x28\xb5\x2f\xfd':
        proc = subprocess.run(['zstd', '-dc'], input=payload, capture_output=True, check=True)
        return proc.stdout
    if payload[:2] == b'\x1f\x8b':
        return gzip.decompress(payload)
    if payload[:6] == b'\xfd7zXZ\x00':
        return lzma.decompress(payload)
    if payload[:3] == b'BZh':
        return bz2.decompress(payload)
    return payload


def extract_files(data, wanted):
    """Extract the wanted paths from a cpio (newc) payload in memory."""
    wanted = {p.lstrip('/') for p in wanted}
    found = {}
    pos = 0
    while pos + 110 <= len(data):
        if data[pos : pos + 6] != b'070701':
            break
        fields = [int(data[pos + 6 + i * 8 : pos + 14 + i * 8], 16) for i in range(13)]
        namesize, filesize = fields[11], fields[6]
        name_start = pos + 110
        name = data[name_start : name_start + namesize - 1].decode('utf-8', 'replace')
        body_start = (name_start + namesize + 3) & ~3
        if name == 'TRAILER!!!':
            break
        if name.lstrip('./') in wanted:
            found[name.lstrip('./')] = data[body_start : body_start + filesize]
        pos = (body_start + filesize + 3) & ~3
    return found


def strip_lua(text):
    """
    Remove %{lua: ...} spans from a macro body.

    Their content is lua code: a %1 inside it is a lua pattern capture,
    not a reference to the macro's argument vector (the __python3 body,
    a gsub pattern, is the canonical example).
    """
    out = []
    i = 0
    while True:
        j = text.find('%{lua:', i)
        if j < 0:
            out.append(text[i:])
            return ''.join(out)
        out.append(text[i:j])
        depth = 0
        k = j + 1
        while k < len(text):
            if text[k] == '{':
                depth += 1
            elif text[k] == '}':
                depth -= 1
                if depth == 0:
                    break
            k += 1
        i = k + 1


def parse_macro_text(text, into):
    """Collect argument-taking macro names defined in one macro file."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if line.startswith('#') or not line.startswith('%'):
            continue
        m = DEFINE_RE.match(line) or DEF_RE.match(line)
        if not m:
            continue
        name, args, body = m.group(1), m.group(2), m.group(3) or ''
        while body.endswith('\\') and i < len(lines):
            body += '\n' + lines[i]
            i += 1
        if name in ('define', 'global'):
            continue
        if args is not None or ARG_REF.search(strip_lua(body)):
            into.add(name)


def collect_macro_names(repo, workdir, binaries):
    """
    Download the given packages of one repository; collect their macro names.

    Every package is verified against the checksum and size the primary
    data publishes for it, then downloaded and read. Identical macro
    file contents are parsed once: several packages ship byte-identical
    copies of a macro file, and a second copy could only produce the
    names the first one produced.
    """
    names = set()
    seen_contents = set()
    files_seen = 0
    for _name, _arch, files, href, size, checksum in binaries:
        dest = os.path.join(workdir, 'rpms', os.path.basename(href))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        fetch(repo + href, dest)
        verify_package(dest, href, checksum, size)
        with open(dest, 'rb') as fh:
            payload = rpm_payload(fh.read())
        found = extract_files(payload, files)
        for content in found.values():
            digest = hashlib.sha256(content).digest()
            if digest in seen_contents:
                continue
            seen_contents.add(digest)
            files_seen += 1
            parse_macro_text(content.decode('utf-8', 'replace'), names)
    return names, files_seen


def repo_macro_names(repo, workdir):
    """Run the full enumeration over one repository; return its names and revision."""
    hrefs, checks, revision = repodata_hrefs(repo, workdir)
    owners = macro_packages(repo, workdir, hrefs, checks)
    locations = package_locations(repo, workdir, hrefs, checks)
    binaries = all_binaries(owners, locations)
    names, files_seen = collect_macro_names(repo, workdir, binaries)
    return names, revision, len(binaries), files_seen


def builtin_macros():
    """Collect the builtin macro names from the local rpm --showrc."""
    out = subprocess.run(['rpm', '--showrc'], capture_output=True, text=True, check=True).stdout
    return {m.group(1) for line in out.splitlines() if (m := BUILTIN_RE.match(line))}


def read_existing(path):
    """Read the distro names and builtin section of an existing output."""
    distro, builtins, section = set(), set(), None
    if not path or not os.path.exists(path):
        return distro, builtins
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if line.startswith(BUILTINS_MARKER):
            section = builtins
        elif line and not line.startswith('#'):
            (section if section is not None else distro).add(line)
    return distro, builtins


def main():
    """Generate the snapshot: parse the repository, write the name list."""
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=DEFAULT_REPO)
    ap.add_argument(
        '--fedora-repo',
        default=DEFAULT_FEDORA_REPO,
        help='Fedora Rawhide repository unioned into the snapshot; '
        'pass an empty string to build from --repo only',
    )
    ap.add_argument(
        '--workdir', default=os.path.join(tempfile.gettempdir(), 'spec-cleaner-macro-functions')
    )
    ap.add_argument('--out', default='spec_cleaner/data/macro_functions.txt')
    ap.add_argument(
        '--keep-builtins',
        action='store_true',
        help='carry the builtin section of the existing output '
        'over instead of reading rpm --showrc',
    )
    args = ap.parse_args()

    os.makedirs(args.workdir, exist_ok=True)
    names, revision, binaries, files_seen = repo_macro_names(args.repo, args.workdir)

    fedora_revision = None
    fedora_binaries = 0
    if args.fedora_repo:
        fedora_workdir = os.path.join(args.workdir, 'fedora')
        os.makedirs(fedora_workdir, exist_ok=True)
        f_names, fedora_revision, fedora_binaries, f_files = repo_macro_names(
            args.fedora_repo, fedora_workdir
        )
        names |= f_names
        files_seen += f_files

    _old, kept_builtins = read_existing(args.out)
    if args.keep_builtins and kept_builtins:
        builtins = kept_builtins
        builtin_note = 'carried over from the previous snapshot'
    else:
        try:
            builtins = builtin_macros()
            rpm_version = subprocess.run(
                ['rpm', '--version'], capture_output=True, text=True
            ).stdout.strip()
            builtin_note = f'read from {rpm_version}'
        except (OSError, subprocess.CalledProcessError):
            # No usable rpm on this host (the release runners have none):
            # carry the recorded builtins over rather than dropping them.
            builtins = kept_builtins
            builtin_note = 'carried over from the previous snapshot (no rpm here)'
    names -= builtins
    with open(args.out, 'w', encoding='utf-8') as fh:
        fh.write(
            '# Argument-taking rpm macros from the openSUSE Tumbleweed '
            f'snapshot {revision}, fetched {date.today().isoformat()}\n'
        )
        if fedora_revision is not None:
            fh.write(
                '# Unioned with Fedora Rawhide '
                f'snapshot {fedora_revision}, fetched {date.today().isoformat()}\n'
            )
        fh.write(
            '# Generated by generate-macro-functions.py; refresh with '
            "'make spec_cleaner/data/macro_functions.txt'.\n"
        )
        for name in sorted(names):
            fh.write(name + '\n')
        fh.write(f'{BUILTINS_MARKER} ({builtin_note})\n')
        for name in sorted(builtins):
            fh.write(name + '\n')
    package_counts = f'{binaries} macro packages'
    if fedora_revision is not None:
        package_counts += f' + {fedora_binaries} Fedora macro packages'
    print(
        f'wrote {args.out}: {len(names) + len(builtins)} names '
        f'({package_counts}, {files_seen} macro files, '
        f'{len(builtins)} builtins)'
    )


if __name__ == '__main__':
    main()
