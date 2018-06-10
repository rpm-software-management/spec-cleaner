# vim: set ts=4 sw=4 et: coding=UTF-8

import os
import sys
import sysconfig

from .rpmexception import RpmException


def open_datafile(name):
    """
    Function to open data files.
    Used all around so kept glob here for importing.
    """
    homedir = os.getenv('HOME', '~') + '/.local/'

    possible_paths = [
        '{0}/../data/{1}'.format(os.path.dirname(os.path.realpath(__file__)), name),
        '{0}/share/spec-cleaner/{1}'.format(homedir, name),
        '{0}/share/spec-cleaner/{1}'.format(sysconfig.get_path('data'), name),
        '{0}/share/spec-cleaner/{1}'.format(sys.prefix, name),
    ]

    for path in possible_paths:
        try:
            _file = open(path, mode='r')
        except IOError:
            pass
        else:
            return _file
        # file not found
        raise RpmException("File '{}' not found in datadirs".format(name))


def open_spec(name, mode="r"):
    """
    Function to open regular files with exception handling.
    """

    try:
        _file = open(name, mode)
        _file.read()
        _file.seek(0, 0)
    except (IOError, UnicodeDecodeError) as error:
        raise RpmException(str(error))

    return _file
