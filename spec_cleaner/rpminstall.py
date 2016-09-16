# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmInstall(Section):

    '''
        Remove commands that wipe out the build root.
        Replace %makeinstall (suse-ism).
    '''

    def add(self, line):
        line = self._complete_cleanup(line)

        # we do not want to cleanup buildroot, it is already clean
        if self.reg.re_clean.search(line):
            return

        line = self.reg.re_jobs.sub(' %{?_smp_mflags}', line)
        if not self.minimal:
            line = self._replace_remove_la(line)
            line = self._replace_install_command(line)

        Section.add(self, line)

    def _replace_install_command(self, line):
        """
        Replace various install commands with one unified mutation
        """
        make_install = '%make_install'

        # do not use install macros as we have trouble with it for now
        # we can convert it later on
        if self.reg.re_install.match(line):
            line = make_install

        # we can deal with additional params for %makeinstall so replace that
        line = line.replace('%makeinstall', make_install)

        return line

    def _replace_remove_la(self, line):
        """
        Replace all known variations of la file deletion with one unified
        """
        if (self.reg.re_rm.search(line) and len(self.reg.re_rm_double.split(line)) == 1) or \
                (self.reg.re_find.search(line) and len(self.reg.re_find_double.split(line)) == 2):
            line = 'find %{buildroot} -type f -name "*.la" -delete -print'
        return line
