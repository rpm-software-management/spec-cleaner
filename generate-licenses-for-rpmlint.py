#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(
    description='Generate TOML configuration file with valid licenses.'
)
parser.add_argument('output', help='Output file')
parser.add_argument('-s', '--suse', action='store_true', help='Add SUSE exceptions')

args = parser.parse_args()

with open(args.output, 'w') as wfile:
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
        if line.startswith('#'):
            continue
        wfile.write(f'    "{line.strip()}",\n')
    wfile.write(']\n')
