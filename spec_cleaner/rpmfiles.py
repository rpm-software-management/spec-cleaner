# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmFiles(Section):

    """
        Class that does replacements on the %files section.
    """

    comment_present = False

    def add(self, line):
        line = self._complete_cleanup(line)
        line = self.strip_useless_spaces(line)
        line = self._remove_doc_on_man(line)
        line = self._move_license_from_doc(line)
        # we only get empty %doc left over
        if line == '%doc ':
            return

        if not self.minimal:
            # prune obsolete defattr that is default
            if self.reg.re_defattr.match(line):
                return
            line = self._set_man_compression(line)

        # toss out empty lines if there are more than one in succession
        if line == '' and (not self.previous_line or self.previous_line == ''):
            return

        Section.add(self, line)

    @staticmethod
    def _remove_doc_on_man(line):
        """
        Remove all %doc %_mandir to -> %_mandir as it is pointless to do twice
        """
        line = line.replace("%doc %{_mandir}", "%{_mandir}", 1)
        line = line.replace("%doc %{_infodir}", "%{_infodir}", 1)
        return line

    def _set_man_compression(self, line):
        """
        Set proper compression suffix on man/info pages, instead of .gz/.* use
        the proper macro variable
        """
        if line.startswith("%{_mandir}"):
            line = self.reg.re_man_compression.sub(r'\1%{?ext_man}', line)
        if line.startswith("%{_infodir}"):
            line = self.reg.re_info_compression.sub('.info%{?ext_info}', line)
        return line

    def _move_license_from_doc(self, line):
        if line.startswith("%doc") and self.reg.re_doclicense.search(line):
            match = ''
            while self.reg.re_doclicense.search(line):
                match += self.reg.re_doclicense.search(line).group()
                line = self.reg.re_doclicense.sub('', line, 1)
            Section.add(self, "%license {}".format(match))
        return line
