# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section

class RpmPrep(Section):
    '''
        Try to simplify to %setup -q when possible.
        Replace %patch with %patch0
    '''


    re_patch = re.compile('^%patch\s*(.*)-P\s*(\d*)\s*(.*)')


    def add(self, line):
        if line.startswith('%setup'):
            cmp_line = line.replace(' -q', '')
            cmp_line = cmp_line.replace(' -n %{name}-%{version}', '')
            line = self.strip_useless_spaces(cmp_line)

        if self.re_patch.match(line):
            match = self.re_patch.match(line)
            line = self.strip_useless_spaces('%%patch%s %s %s' % (match.group(2), match.group(1), match.group(3)))
        elif line.startswith('%patch ') or line == '%patch':
            line = line.replace('%patch','%patch0')

        line = embrace_macros(line)
        Section.add(self, line)
