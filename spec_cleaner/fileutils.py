# vim: set ts=4 sw=4 et: coding=UTF-8

import os
import sys
import sysconfig
from io import StringIO
from typing import IO

from .rpmexception import RpmExceptionError


def datafile_paths(name: str) -> tuple[str, ...]:
    """
    Candidate locations of a shipped data file, in lookup order.

    Args:
        name: A string representing the name of the datafile to open.

    Returns:
        The paths open_datafile tries, first match wins.
    """
    # HOME may be unset or empty, then the passwd entry is the home to use
    homedir = os.environ.get('HOME') or os.path.expanduser('~')
    homedir = homedir.rstrip('/') + '/.local/'

    # the data files are shipped inside the package itself so that pip
    # installs work on every install scheme (venv, --user, --target,
    # macOS, ...) instead of relying on sysconfig data paths (gh#292)
    return (
        f'{os.path.dirname(os.path.realpath(__file__))}/data/{name}',
        f'{homedir}/share/spec-cleaner/{name}',
        f'{sysconfig.get_path("data")}/share/spec-cleaner/{name}',
        f'{sys.prefix}/share/spec-cleaner/{name}',
    )


def stat_datafile(name: str) -> tuple[str, int, int] | None:
    """
    Identify the data file open_datafile would open, without reading it.

    Args:
        name: A string representing the name of the datafile to open.

    Returns:
        The real path, mtime and size of the first candidate that exists,
        or None when no candidate exists.
    """
    for path in datafile_paths(name):
        try:
            stat = os.stat(path)
        except OSError:
            continue
        return (os.path.realpath(path), stat.st_mtime_ns, stat.st_size)
    return None


def open_datafile(name: str) -> IO[str]:
    """
    Open data files.

    Used all around so kept glob here for importing.

    Args:
        name: A string representing the name of the datafile to open.

    Raises:
        RpmExceptionError if the file is not found in predefined datadirs.
    """
    for path in datafile_paths(name):
        try:
            _file = open(path, encoding='utf-8')
        except OSError:
            continue
        try:
            # the decoding is lazy, so a file that is not UTF-8 only fails once
            # somebody reads it; fail here, where the path is still known
            _file.read()
            _file.seek(0)
        except UnicodeDecodeError as error:
            _file.close()
            raise RpmExceptionError(f"File '{name}' is not valid UTF-8: {error}") from error
        except OSError:
            _file.close()
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
