# vim: set ts=4 sw=4 et: coding=UTF-8

# We basically extend rpmcheck
from rpmcheck import RpmCheck


class RpmBuild(RpmCheck):
    """
        Replace various troublemakers in build phase
    """

    def add(self, line):
        # if user uses cmake directly just recommend him using the macros
        if line.startswith('cmake'):
            self.lines.append('# FIXME: you should use %%cmake macros')

        RpmCheck.add(self, line)
