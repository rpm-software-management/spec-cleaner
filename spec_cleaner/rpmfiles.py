# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section


class RpmFiles(Section):
    """
        Replace additional /usr, /etc and /var because we're sure we can use
        macros there.

        Replace '%dir %{_includedir}/mux' and '%{_includedir}/mux/*' with
        '%{_includedir}/mux/'
    """

    def __init__(self, specfile):
        Section.__init__(self, specfile)
        self.dir_on_previous_line = None


    def add(self, line):
        line = self.reg.re_etcdir.sub(r'\1%{_sysconfdir}/', line)
        line = self.reg.re_usrdir.sub(r'\1%{_prefix}/', line)
        line = self.reg.re_vardir.sub(r'\1%{_localstatedir}/', line)

        if self.dir_on_previous_line:
            if line == self.dir_on_previous_line + '/*':
                Section.add(self, self.dir_on_previous_line + '/')
                self.dir_on_previous_line = None
                return
            else:
                Section.add(self, '%dir ' + self.dir_on_previous_line)
                self.dir_on_previous_line = None

        match = self.reg.re_dir.match(line)
        if match:
            self.dir_on_previous_line = match.group(1)
            return

        Section.add(self, line)
