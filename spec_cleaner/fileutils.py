# vim: set ts=4 sw=4 et: coding=UTF-8

import os
import sys
import sysconfig
from io import StringIO
from typing import IO

from .rpmexception import RpmExceptionError


def open_datafile(name: str) -> IO[str]:
    """
    Open data files.

    Used all around so kept glob here for importing.

    Args:
        name: A string representing the name of the datafile to open.

    Raises:
        RpmExceptionError if the file is not found in predefined datadirs.
    """
    homedir = os.getenv('HOME', '~') + '/.local/'

    possible_paths = (
        '{0}/../data/{1}'.format(os.path.dirname(os.path.realpath(__file__)), name),
        '{0}/share/spec-cleaner/{1}'.format(homedir, name),
        '{0}/share/spec-cleaner/{1}'.format(sysconfig.get_path('data'), name),
        '{0}/share/spec-cleaner/{1}'.format(sys.prefix, name),
    )

    for path in possible_paths:
        try:
            _file = open(path, mode='r')
        except OSError:
            pass
        else:
            return _file
    # file not found
    raise RpmExceptionError("File '{}' not found in datadirs".format(name))


def open_stringio_spec(name: str) -> IO[str]:
    """
    Open regular files with exception handling.

    Args:
        name: A string with the file name.

    Returns:
        A file object.

    Raises:
        RpmExceptionError if the file is not readable.
    """
    data = StringIO()
    try:
        with open(name, mode='r') as f:
            data.write(f.read())
            data.seek(0, 0)
    except (IOError, UnicodeDecodeError) as error:
        raise RpmExceptionError(str(error))
    return data
