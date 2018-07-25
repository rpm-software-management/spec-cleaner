# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmScriptlets(Section):

    """
        Do %post -p /sbin/ldconfig when only scriplet command is /sbin/ldconfig
    """

    def add(self, line):
        line = self._complete_cleanup(line)
        line = self._remove_deprecated_ldconfig(line)
        Section.add(self, line)

    def _remove_deprecated_ldconfig(self, line):
        line = self.reg.re_ldconfig.sub('/sbin/ldconfig', line)
        return line

    def output(self, fout, newline=True, new_class=None):
        if not self.minimal:
            self._collapse_multiline_ldconfig()
        Section.output(self, fout, newline, new_class)

    def _collapse_multiline_ldconfig(self):
        # if we have 2 lines or rest of them are empty, pop those
        for i in reversed(self.lines):
            if i:
                break
            else:
                self.lines.pop()
        if len(self.lines) == 2:
            if self.lines[1] == '/sbin/ldconfig':
                pkg = self.lines[0]
                self.lines = []
                self.lines.append('{0} -p /sbin/ldconfig'.format(pkg))
