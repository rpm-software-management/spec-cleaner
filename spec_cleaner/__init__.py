# vim: set ts=4 sw=4 et: coding=UTF-8

# Copyright (c) 2015, SUSE LINUX Products GmbH, Nuernberg, Germany
# All rights reserved.
# See COPYING for details.

"""Spec-cleaner formatting module."""

import argparse
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

from .rpmcleaner import RpmSpecCleaner
from .rpmexception import RpmExceptionError, RpmWrongArgsError

__version__ = '1.2.3'


def process_args(argv: List[str]) -> Dict[str, Any]:
    """
    Parse and process commandline arguments.

    Args:
        argv: A list of passed arguments.

    Returns:
        A dict mapping arguments to the corresponding values.

    Raises:
        RpmWrongArgsError: If the specfile doesn't exist or
                      if the output file already exists but '--force' option (overwrite the output) wasn't used.
    """
    parser = argparse.ArgumentParser(
        prog='spec-cleaner',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Cleans the given spec file according to style guide and returns the result. If "#nospeccleaner"'
        'tag is used in the spec file than the spec file will not be cleaned.',
    )

    # Make the -d, -i, and -o exclusive as we can do only one of those
    output_group = parser.add_mutually_exclusive_group()

    parser.add_argument('specfile', metavar='SPEC', type=str, help='spec file to beautify')
    parser.add_argument(
        '-c',
        '--cmake',
        action='store_true',
        help='convert dependencies to their cmake() counterparts, requires bit more of cleanup in spec afterwards.',
    )
    output_group.add_argument(
        '-d',
        '--diff',
        action='store_true',
        help='run the diff program to show differences between new and original specfile.',
    )
    parser.add_argument(
        '--diff-prog', default='vimdiff', help='specify the diff binary to call with diff option.',
    )
    parser.add_argument(
        '-f', '--force', action='store_true', help='overwrite the output file if already exist.',
    )
    output_group.add_argument(
        '-i',
        '--inline',
        action='store_true',
        help='inline the changes directly to the parsed file.',
    )
    parser.add_argument(
        '-m',
        '--minimal',
        action='store_true',
        help='run in minimal mode that does not do anything intrusive (ie. just sets the Copyright)',
    )
    parser.add_argument(
        '--no-curlification',
        action='store_true',
        help='do not convert variables bracketing (%%{macro}) and keep it as it was on the input',
    )
    parser.add_argument(
        '--no-copyright',
        action='store_true',
        help='do not include official SUSE copyright hear and just keep what is present',
    )
    parser.add_argument(
        '--remove-groups', action='store_true', help='remove groups from the specfile.'
    )
    parser.add_argument(
        '--copyright-year',
        metavar='YYYY',
        type=int,
        default=datetime.now().year,
        help='year to insert into the copyright header when re-generating it',
    )
    output_group.add_argument(
        '-o', '--output', default='', help='specify the output file for the cleaned spec content.',
    )
    parser.add_argument(
        '-p',
        '--pkgconfig',
        action='store_true',
        help='convert dependencies to their pkgconfig() counterparts, requires bit more of cleanup in spec afterwards.',
    )
    parser.add_argument(
        '--perl',
        action='store_true',
        help='convert dependencies to their perl() counterparts, highly expansive use carefully',
    )
    parser.add_argument(
        '-t',
        '--tex',
        action='store_true',
        help='convert dependencies to their tex() counterparts, requires verification of the output afterwards.',
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__,
        help='show package version and exit',
    )
    parser.add_argument(
        '-k', '--keep-space', action='store_true', help='keep empty lines in preamble intact.',
    )

    # print help if there is no argument
    if len(argv) < 1:
        parser.print_help()
        sys.exit(0)

    options = parser.parse_args(args=argv)

    # the spec must exist for us to do anything
    if not os.path.exists(options.specfile):
        raise RpmWrongArgsError('{0} does not exist.'.format(options.specfile))

    # the path for output must exist and the file must not be there unless
    # force is specified
    if options.output:
        options.output = os.path.expanduser(options.output)
        if not options.force and os.path.exists(options.output):
            raise RpmWrongArgsError('{0} already exists.'.format(options.output))

    # convert options to dict
    options_dict = vars(options)
    return options_dict


def main() -> int:
    """
    Run main function.

    It calls argument parsing ensures their sanity and then creates
    RpmSpecCleaner object that works with passed spec file.
    """
    try:
        options = process_args(sys.argv[1:])
    except RpmWrongArgsError as exception:
        sys.stderr.write('ERROR: {0}\n'.format(exception))
        return 1

    try:
        cleaner = RpmSpecCleaner(options)
        cleaner.run()
    except RpmExceptionError as exception:
        sys.stderr.write('ERROR: {0}\n'.format(exception))
        return 1

    return 0
