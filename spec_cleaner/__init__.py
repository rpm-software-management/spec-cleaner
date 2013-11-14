#!/usr/bin/env python
# vim: set ts=4 sw=4 et: coding=UTF-8

# Copyright (c) 2013, SUSE LINUX Products GmbH, Nuernberg, Germany
# All rights reserved.
# See COPYING for details.

__version__ = '0.4'

import os
import sys
import argparse

from rpmexception import RpmException
from cleaner import RpmSpecCleaner

def process_args(argv):
    """
    Process the parsed arguments and return the result
    :param argv: passed arguments
    """

    parser = argparse.ArgumentParser(prog='spec-cleaner',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Cleans the given spec file according to some arbitrary style guide and prints the result.')

    # Make the -d, -i, and -o exclusive as we can do only one of those
    output_group = parser.add_mutually_exclusive_group()

    parser.add_argument('spec', metavar='SPEC', type=str,
                        help='spec file to beautify')
    output_group.add_argument('-d', '--diff', action='store_true', default=False,
                        help='run the diff program to show differences between new and orginal specfile.')
    parser.add_argument('-p', '--diff-prog', default='vimdiff',
                        help='specify the diff binary to call with diff option.')
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='overwrite the output file if already exist.')
    output_group.add_argument('-i', '--inline', action='store_true', default=False,
                        help='inline the changes directly to the parsed file.')
    output_group.add_argument('-o', '--output', default='',
                        help='specify the output file for the cleaned spec content.')
    parser.add_argument('-v', '--version', action='version', version=__version__,
                        help='show package version and exit')

    # print help if there is no argument
    if len(argv) < 1:
        parser.print_help()
        return 1

    return parser.parse_args(args=argv)

def main(argv):
    """
    Main function that calls argument parsing and then creates
    RpmSpecCleaner object that works with passed spec file.
    :param argv: passed arguments
    """

    options = process_args(argv)

    try:
        cleaner = RpmSpecCleaner(options.spec,
                                 os.path.expanduser(options.output),
                                 options.inline,
                                 options.force,
                                 options.diff,
                                 options.diff_prog)
        cleaner.run()
    except RpmException, e:
        print >> sys.stderr, '%s' % e
        return 1

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        pass
