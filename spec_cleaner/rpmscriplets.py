# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmScriptlets(Section):

    '''
        Do %post -p /sbin/ldconfig when only scriplet command is /sbin/ldconfig
    '''

    def output(self, fout, newline=True, new_class=None):
        if not self.minimal:
            self._collapse_multiline_ldconfig(newline)
        Section.output(self, fout, newline, new_class)

    def _collapse_multiline_ldconfig(self, newline):
        nolines = len(self.lines)
        # if we have 2 or 3 lines where last one is empty
        if nolines == 2 or (nolines == 3 and self.lines[2] == ''):
            if self.lines[0] != '' and self.lines[1] == '':
                self.lines.pop()
            if len(self.lines) >= 2:
                if self.lines[1] == '/sbin/ldconfig':
                    pkg = self.lines[0]
                    self.lines = []
                    self.lines.append('{0} -p /sbin/ldconfig'.format(pkg))
