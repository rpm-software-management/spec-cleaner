# vim: set ts=4 sw=4 et: coding=UTF-8

import os


class FileUtils:
    def open_datafile(self, FILE):
        """
        Function to open data files.
        Used all around so kept glob here for importing.
        """
        try:
            f = open('/usr/share/spec-cleaner/{0}'.format(FILE), 'r')
        except IOError:
            # the .. is appended as we are in spec_cleaner sub_folder
            f = open('{0}/{1}'.format(os.path.dirname(os.path.realpath(__file__)) + '/../data/', FILE), 'r')

        return f
