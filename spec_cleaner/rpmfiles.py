# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section


class RpmFiles(Section):
    """
        Class that does replacements on the %files section.
    """

    def add(self, line):
        line = self._complete_cleanup(line)
        line = self.strip_useless_spaces(line)
        # if it is 2nd line and it is not defattr just set there some default
        if self.previous_line and \
                self.previous_line.startswith('%files') and \
                not line.startswith('%defattr'):
            self.lines.append('%defattr(-,root,root)')

        # toss out empty lines if there are more than one in succession
        if line == '' and ( not self.previous_line or self.previous_line == ''):
            return

        Section.add(self, line)
