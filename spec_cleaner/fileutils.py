# vim: set ts=4 sw=4 et: coding=UTF-8

import os
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

        try:
            # the .. is appended as we are in spec_cleaner sub_folder
            _file = open('{0}/../data/{1}'.format(os.path.dirname(os.path.realpath(__file__)), name), 'r')
        except IOError:
            # try system dir
            try:
                # usually /usr
                path = sysconfig.get_path('data')
                _file = open('{0}/share/spec-cleaner/{1}'.format(path, name), 'r')
            except IOError as error:
                raise RpmException(str(error))

        self.f = _file

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
