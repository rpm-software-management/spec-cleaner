# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section

class RpmPrep(Section):
    '''
        Try to simplify to %setup -q when possible.
        Replace %patch with %patch0
    '''


    def add(self, line):
        if line.startswith('%setup'):
            line = line.replace(' -qn', '-q -n')
            line = line.replace(' -q', '')
            line = line.replace(' -n %{name}-%{version}', '')
            line = self.strip_useless_spaces(line)

        if self.reg.re_patch.match(line):
            match = self.re_patch.match(line)
            line = self.strip_useless_spaces('%%patch%s %s %s' % (match.group(2), match.group(1), match.group(3)))
        elif line.startswith('%patch ') or line == '%patch':
            line = line.replace('%patch','%patch0')

        Section.add(self, line)
