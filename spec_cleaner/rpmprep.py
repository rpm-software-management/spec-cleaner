# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmPrep(Section):

    '''
        Try to simplify to %setup -q when possible.
        Replace %patch with %patch0
    '''

    def add(self, line):
        line = self._complete_cleanup(line)
        if not self.minimal:
            line = self._cleanup_setup(line)
            line = self._prepare_patch(line)
        Section.add(self, line)

    def _cleanup_setup(self, line):
        """
        Remove the useless stuff from %setup line
        """
        # NOTE: not using regexp as this covers 99% cases for now
        if line.startswith('%setup'):
            line = line.replace(' -qn', ' -q -n')
            line = line.replace(' -q', '')
            line = self.reg.re_setup.sub(' ', line)
            line = self.strip_useless_spaces(line)
            line = line.replace('%setup', '%setup -q')

        return line

    def _prepare_patch(self, line):
        """
        Convert patchlines to something pretty
        """
        # -p0 is default
        line = line.replace('-p0', '')
        # %patch0 is desired
        if (line.startswith('%patch ') or line == '%patch') and '-P' not in line:
            line = line.replace('%patch', '%patch0')

        # convert the %patch -P 50 -p10 to %patch50 -p10
        # this apply only if there is ONE -P on the line, not multiple ones
        if self.reg.re_patch_prep.match(line):
            match = self.reg.re_patch_prep.match(line)
            line = self.strip_useless_spaces('%%patch%s %s %s' % (match.group(2), match.group(1), match.group(3)))

        return line
