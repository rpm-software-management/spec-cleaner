# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section


class RpmInstall(Section):
    '''
        Remove commands that wipe out the build root.
        Use %make_install macro.
        Replace %makeinstall (suse-ism).
    '''

    def add(self, line):
        install_command = 'make DESTDIR=%{buildroot} install %{?_smp_mflags}'

        line = self._complete_cleanup(line)
        line = self._replace_remove_la(line)

        # we do not want to cleanup buildroot, it is already clean
        if self.reg.re_clean.search(line):
            return

        # do not use install macros as we have trouble with it for now
        # we can convert it later on
        if self.reg.re_install.match(line):
            line = install_command

        Section.add(self, line)


    def _replace_remove_la(self, line):
        """
        Replace all known variations of la file deletion with one unified
        """
        if (self.reg.re_rm.search(line) and len(self.reg.re_rm_double.split(line)) == 1) or \
                (self.reg.re_find.search(line) and len(self.reg.re_find_double.split(line)) == 2):
            line = 'find %{buildroot} -type f -name "*.la" -delete -print'
        return line
