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

    def open_datafile(self, FILE):
        """
        Function to open data files.
        Used all around so kept glob here for importing.
        """

        try:
            f = open('{0}/../data/{1}'.format(os.path.dirname(os.path.realpath(__file__)), FILE), 'r')
        except IOError:
            # the .. is appended as we are in spec_cleaner sub_folder
            try:
                f = open('/usr/share/spec-cleaner/{0}'.format(FILE), 'r')
            except IOError as e:
                raise RpmException(e)

        self.f = f

    def open(self, FILE, mode):
        """
        Function to open regular files with exception handling.
        """

        try:
            f = open(FILE, mode)
        except IOError as error:
            raise RpmException(error)

        self.f = f

    def close(self):
        """
        Just wrapper for closing the file
        """

        if self.f:
            self.f.close()

    def __del__(self):
        self.close()
        self.f = None
