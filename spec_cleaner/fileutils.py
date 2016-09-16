# vim: set ts=4 sw=4 et: coding=UTF-8

import os
import sys
import sysconfig

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

        homedir = os.getenv('HOME') + '/.local/'

        possible_paths = [
            '{0}/../data/{1}'.format(os.path.dirname(os.path.realpath(__file__)), name),
            '{0}/share/spec-cleaner/{1}'.format(homedir, name),
            '{0}/share/spec-cleaner/{1}'.format(sysconfig.get_path('data'), name),
            '{0}/share/spec-cleaner/{1}'.format(sys.prefix, name),
        ]
        for path in possible_paths:
            try:
                _file = open(path, 'r')
            except IOError:
                pass
            else:
                self.f = _file
                return
        # file not found
        raise RpmException("File '{0}' not found in datadirs".format(name))

    def open(self, name, mode):
        """
        Function to open regular files with exception handling.
        """

        try:
            _file = open(name, mode)
        except IOError as error:
            raise RpmException(str(error))

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
