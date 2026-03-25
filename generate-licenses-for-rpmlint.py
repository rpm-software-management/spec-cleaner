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
    wfile.write('# Generated with %s script from spec-cleaner:\n' % script_name)
    wfile.write('# URL: https://github.com/rpm-software-management/spec-cleaner\n\n')
    wfile.write('ValidLicenses = [\n')
    suse_exceptions = []
    for line in open('data/licenses_changes.txt').readlines():
        if line.startswith('First line'):
            continue
        old_name, new_name = line.strip().split('\t')
        wfile.write(f'    "{old_name}",\n')
        if new_name.startswith('LicenseRef-SUSE') or new_name.startswith('SUSE-'):
            suse_exceptions.append(new_name)
    if args.suse:
        wfile.write('    # SUSE EXCEPTIONS\n')
        for name in suse_exceptions:
            wfile.write(f'    "{name}",\n')
    wfile.write(']\n')
