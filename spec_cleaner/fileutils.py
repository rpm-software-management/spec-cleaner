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

    # the data files are shipped inside the package itself so that pip
    # installs work on every install scheme (venv, --user, --target,
    # macOS, ...) instead of relying on sysconfig data paths (gh#292)
    possible_paths = (
        f'{os.path.dirname(os.path.realpath(__file__))}/data/{name}',
        f'{homedir}/share/spec-cleaner/{name}',
        f'{sysconfig.get_path("data")}/share/spec-cleaner/{name}',
        f'{sys.prefix}/share/spec-cleaner/{name}',
    )

    for path in possible_paths:
        try:
            _file = open(path, encoding='utf-8')
        except OSError:
            pass
        else:
            return _file
    # file not found
    raise RpmExceptionError(f"File '{name}' not found in datadirs")


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
        with open(name, encoding='utf-8') as f:
            data.write(f.read())
            data.seek(0, 0)
    except (OSError, UnicodeDecodeError) as error:
        raise RpmExceptionError(str(error)) from error
    return data
