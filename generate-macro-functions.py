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

The repository defaults to the openSUSE Tumbleweed oss repository, the
development distribution the Factory corpus is built from.  Only
python3 and the zstd binary are needed; rpm payloads are extracted
directly, without rpm2cpio/cpio.
"""

import argparse
import bz2
import gzip
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

DEFAULT_REPO = 'http://download.opensuse.org/tumbleweed/repo/oss/'

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


def repodata_hrefs(repo, workdir):
    """Read repomd.xml; return the data hrefs and the snapshot revision."""
    repomd = fetch(repo + 'repodata/repomd.xml', os.path.join(workdir, 'repomd.xml'))
    tree = ET.parse(repomd)
    hrefs = {}
    for data in tree.getroot().iter(R_TAG + 'data'):
        hrefs[data.get('type')] = data.find(R_TAG + 'location').get('href')
    rev_el = tree.getroot().find(R_TAG + 'revision')
    return hrefs, rev_el.text if rev_el is not None else 'unknown'


def macro_packages(repo, workdir, hrefs):
    """Map package identity -> [macro file paths] from the filelists."""
    path = fetch(
        repo + hrefs['filelists'], os.path.join(workdir, os.path.basename(hrefs['filelists']))
    )
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


def package_locations(repo, workdir, hrefs):
    """Map (name, arch) -> (location href, package size) from the primary data."""
    path = fetch(repo + hrefs['primary'], os.path.join(workdir, os.path.basename(hrefs['primary'])))
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
    return locations


def pick_binaries(owners, locations):
    """
    One binary per package name: noarch first, then x86_64, then any arch.

    Packages whose macro files are all provided by an already picked,
    smaller package are skipped: several packages ship the same macro
    file (cmake-full and cmake-mini both ship macros.cmake) and one copy
    is enough to read its definitions.
    """
    by_name = {}
    for (name, arch), files in owners.items():
        by_name.setdefault(name, []).append((arch, files))
    candidates = []
    for name, variants in by_name.items():
        variants.sort(key=lambda v: (v[0] != 'noarch', v[0] != 'x86_64', v[0]))
        arch, files = variants[0]
        loc = locations.get((name, arch))
        if loc:
            candidates.append((loc[1], name, arch, files, loc[0]))
    picked = {}
    covered = set()
    for size, name, arch, files, href in sorted(candidates):
        if all(f in covered for f in files):
            continue
        covered.update(files)
        picked[name] = (arch, files, href, size)
    return picked


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
    hrefs, revision = repodata_hrefs(args.repo, args.workdir)
    owners = macro_packages(args.repo, args.workdir, hrefs)
    locations = package_locations(args.repo, args.workdir, hrefs)
    picked = pick_binaries(owners, locations)

    names = set()
    files_seen = 0
    for name in sorted(picked):
        arch, files, href, size = picked[name]
        dest = os.path.join(args.workdir, 'rpms', os.path.basename(href))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        fetch(args.repo + href, dest)
        with open(dest, 'rb') as fh:
            payload = rpm_payload(fh.read())
        found = extract_files(payload, files)
        files_seen += len(found)
        for content in found.values():
            parse_macro_text(content.decode('utf-8', 'replace'), names)

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
        fh.write(
            '# Generated by generate-macro-functions.py; refresh with '
            "'make spec_cleaner/data/macro_functions.txt'.\n"
        )
        for name in sorted(names):
            fh.write(name + '\n')
        fh.write(f'{BUILTINS_MARKER} ({builtin_note})\n')
        for name in sorted(builtins):
            fh.write(name + '\n')
    print(
        f'wrote {args.out}: {len(names) + len(builtins)} names '
        f'({len(picked)} macro packages, {files_seen} macro files, '
        f'{len(builtins)} builtins)'
    )


if __name__ == '__main__':
    main()
