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

    re_etcdir = re.compile('(^|\s)/etc/')
    re_usrdir = re.compile('(^|\s)/usr/')
    re_vardir = re.compile('(^|\s)/var/')
    re_dir = re.compile('^\s*%dir\s*(\S+)\s*')

    def __init__(self, re_unbrace_keywords):
        Section.__init__(self, re_unbrace_keywords)
        self.dir_on_previous_line = None


    def add(self, line):
        line = self.re_etcdir.sub(r'\1%{_sysconfdir}/', line)
        line = self.re_usrdir.sub(r'\1%{_prefix}/', line)
        line = self.re_vardir.sub(r'\1%{_localstatedir}/', line)

        if self.dir_on_previous_line:
            if line == self.dir_on_previous_line + '/*':
                Section.add(self, self.dir_on_previous_line + '/')
                self.dir_on_previous_line = None
                return
            else:
                Section.add(self, '%dir ' + self.dir_on_previous_line)
                self.dir_on_previous_line = None

        match = self.re_dir.match(line)
        if match:
            self.dir_on_previous_line = match.group(1)
            return

        Section.add(self, line)
