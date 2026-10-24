#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(
    description='Generate TOML configuration file with valid licenses.'
)
parser.add_argument('output', help='Output file')
parser.add_argument('-s', '--suse', action='store_true', help='Add SUSE exceptions')

args = parser.parse_args()

# Generate into a temporary file next to the output and move it into
# place only once complete: a failure midway (e.g. unreadable input
# data) must never truncate the committed file.
tmp_output = args.output + '.tmp'
try:
    with open(tmp_output, 'w') as wfile:
        script_name = os.path.basename(__file__)
        provenance = 'unknown SPDX revision'
        rows = []
        for line in open('spec_cleaner/data/licenses_changes.txt').readlines():
            if line.startswith('#'):
                if 'SPDX license list' in line:
                    provenance = line.lstrip('# ').rstrip()
                continue
            rows.append(line)
        wfile.write(f'# Generated with {script_name} script from spec-cleaner:\n')
        wfile.write('# URL: https://github.com/rpm-software-management/spec-cleaner\n')
        wfile.write(f'# Source data: {provenance}\n\n')
        wfile.write('ValidLicenses = [\n')
        suse_exceptions = []
        for line in rows:
            old_name, new_name = line.strip().split('\t')
            wfile.write(f'    "{old_name}",\n')
            if new_name.startswith('LicenseRef-SUSE') or new_name.startswith('SUSE-'):
                suse_exceptions.append(new_name)
        if args.suse:
            wfile.write('    # SUSE EXCEPTIONS\n')
            for name in suse_exceptions:
                wfile.write(f'    "{name}",\n')
        wfile.write(']\n\n')
        wfile.write('ValidLicenseExceptions = [\n')
        for line in open('spec_cleaner/data/license_exceptions.txt').readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            wfile.write(f'    "{line}",\n')
        wfile.write(']\n')
    os.replace(tmp_output, args.output)
except BaseException:
    if os.path.exists(tmp_output):
        os.unlink(tmp_output)
    raise
