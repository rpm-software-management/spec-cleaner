# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section


class RpmInstall(Section):
    '''
        Remove commands that wipe out the build root.
        Use %make_install macro.
        Replace %makeinstall (suse-ism).
    '''

    re_rm = re.compile('rm\s+(-?\w?\ ?)*"?(%{buildroot}|\$b)"?/?"?%{_lib(dir)?}.+\.la;?$')
    re_find = re.compile('find\s+"?(%{buildroot}|\$b)("?\S?/?)*\s*.*\s+-i?name\s+["\'\\\\]?\*\.la($|.*[^\\\\]$)')
    re_find_double = re.compile('-i?name')
    re_rm_double = re.compile('(\.|{)a')

    def add(self, line):
        # remove double spaces when comparing the line
        cmp_line = self.strip_useless_spaces(line)
        cmp_line = self.embrace_macros(cmp_line)
        cmp_line = self.replace_buildroot(cmp_line)

        cmp_line = self.replace_remove_la(cmp_line)

        # FIXME: this is very poor patching
        if cmp_line.find('DESTDIR=%{buildroot}') != -1:
            buf = cmp_line.replace('DESTDIR=%{buildroot}', '')
            buf = self.strip_useless_spaces(buf)
            if buf == 'make install' or buf == 'make  install':
                line = '%make_install'
        elif cmp_line == '%{makeinstall}':
            line = '%make_install'
        elif cmp_line == 'rm -rf %{buildroot}':
            return

        Section.add(self, line)


    def replace_remove_la(self, line):
        """
        Replace all known variations of la file deletion with one unified
        """
        if (self.re_rm.search(cmp_line) and len(self.re_rm_double.split(cmp_line)) == 1) or \
                (self.re_find.search(cmp_line) and len(self.re_find_double.split(cmp_line)) == 2):
            line = 'find %{buildroot} -type f -name "*.la" -delete -print'
        return line
