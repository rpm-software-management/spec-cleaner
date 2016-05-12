# vim: set ts=4 sw=4 et: coding=UTF-8

import os

from .rpmexception import RpmException


class FileUtils(object):

    """
    Class working with file operations.
    Read/write..
    """

    # file variable
    f = None

    def open_datafile(self, name):
        """
        Function to open data files.
        Used all around so kept glob here for importing.
        """

        try:
            # the .. is appended as we are in spec_cleaner sub_folder
            _file = open('{0}/../data/{1}'.format(os.path.dirname(os.path.realpath(__file__)), name), 'r')
        except IOError:
            # try venv structure
            try:
                _file = open('{0}/../usr/share/spec-cleaner/{1}'.format(
                    os.path.dirname(os.path.realpath(__file__)), name), 'r')
            except IOError as error:
                # try system dir
                try:
                    _file = open('/usr/share/spec-cleaner/{0}'.format(name), 'r')
                except IOError as error:
                    raise RpmException(error.strerror)

        self.f = _file

    def open(self, name, mode):
        """
        Function to open regular files with exception handling.
        """

        try:
            _file = open(name, mode)
        except IOError as error:
            raise RpmException(error.strerror)

        self.f = _file

    def close(self):
        """
        Just wrapper for closing the file
        """

        if self.f:
            self.f.close()
            self.f = None

    def __del__(self):
        self.close()
        self.f = None
