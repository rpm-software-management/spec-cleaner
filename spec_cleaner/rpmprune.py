# vim: set ts=4 sw=4 et: coding=UTF-8

"""Cleaup classes that drop most of the content"""

from .rpmsection import Section


class RpmClean(Section):

    """Remove clean section"""

    def output(self, fout, newline=True, new_class=None):
        """Do not output anything here"""
        pass


class RpmChangelog(Section):

    """Remove changelog entries."""

    def add(self, line):
        """Only add the first line of changelog

        This translates to adding just %changelog
        """
        if len(self.lines) == 0:
            Section.add(self, "%changelog")
