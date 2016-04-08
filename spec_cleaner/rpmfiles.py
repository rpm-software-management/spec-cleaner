# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmFiles(Section):

    """
        Class that does replacements on the %files section.
    """

    def add(self, line):
        line = self._complete_cleanup(line)
        line = self.strip_useless_spaces(line)

        if not self.minimal:
            self._add_defattr(line)

        # toss out empty lines if there are more than one in succession
        if line == '' and (not self.previous_line or self.previous_line == ''):
            return

        line = self._remove_doc_on_man(line)

        Section.add(self, line)

    def _add_defattr(self, line):
        """
        Add defattr with default values if there is none
        """
        # if it is 2nd line and it is not defattr just set there some default
        if self.previous_line and \
                self.reg.re_spec_files.match(self.previous_line) and \
                not line.startswith('%defattr'):
            self.lines.append('%defattr(-,root,root)')

    def _remove_doc_on_man(self, line):
        """
        Remove all %doc %_mandir to -> %_mandir as it is pointless to do twice
        """
        line = line.replace("%doc %{_mandir}", "%{_mandir}", 1)
        line = line.replace("%doc %{_infodir}", "%{_infodir}", 1)
        return line
