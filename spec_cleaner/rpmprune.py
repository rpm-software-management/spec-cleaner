# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmClean(Section):
    """
        Remove clean section
    """


    def output(self, fout, newline = True):
        pass


class RpmChangelog(Section):
    '''
        Remove changelog entries.
    '''


    def add(self, line):
        # only add the first line (%changelog)
        if len(self.lines) == 0:
            Section.add(self, "%changelog")
