#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(description='Generate TOML configuration file with valid licenses.')
parser.add_argument('output', help='Output file')
parser.add_argument('-s', '--suse', action='store_true', help='Add SUSE exceptions')

args = parser.parse_args()

SUSE_EXCEPTIONS = """
AGPL-3.0 AGPL-3.0+ GFDL-1.1 GFDL-1.1+ GFDL-1.2 GFDL-1.2+ GFDL-1.3 GFDL-1.3+ GPL-3.0-with-GCC-exception \
GPL-2.0-with-classpath-exception GPL-2.0-with-font-exception SUSE-LGPL-2.1+-with-GCC-exception SUSE-NonFree \
GPL-1.0+ GPL-1.0 GPL-2.0+ GPL-2.0 GPL-3.0+ GPL-3.0 LGPL-2.0 LGPL-2.0+ LGPL-2.1+ LGPL-2.1 LGPL-3.0+ LGPL-3.0
"""

with open(args.output, 'w') as wfile:
    script_name = os.path.basename(__file__)
    wfile.write('# Generated with %s script from spec-cleaner:\n' % script_name)
    wfile.write('# URL: https://github.com/rpm-software-management/spec-cleaner\n\n')
    wfile.write('ValidLicenses = [\n')
    added = set()
    for line in open('data/licenses_changes.txt').readlines():
        name = line.strip().split('\t')[0]
        if name not in added:
            wfile.write(f'    "{name}",\n')
            added.add(name)
    if args.suse:
        wfile.write('    # SUSE EXCEPTIONS\n')
        for name in SUSE_EXCEPTIONS.strip().split(' '):
            wfile.write(f'    "{name}",\n')
    wfile.write(']\n')
