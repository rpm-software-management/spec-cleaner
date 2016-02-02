# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmScriptlets(Section):

    '''
        Do %post -p /sbin/ldconfig when only scriplet command is /sbin/ldconfig
    '''

    def output(self, fout, newline=True):
        if not self.minimal:
            newline = self._collapse_multiline_ldconfig(newline)
        Section.output(self, fout, newline)

    def _collapse_multiline_ldconfig(self, newline):
        # if we have 2 or 3 lines where last one is empty
        nolines = len(self.lines)
        if nolines == 1:
            newline=False
        if nolines == 2 or (nolines == 3 and self.lines[2] == ''):
            newline=False
            # if we have two lines and the 2nd is just whitespace, drop it
            if self.lines[0] != '' and self.lines[1] == '':
                self.lines.pop()
            if len(self.lines) >= 2:
                if self.lines[1] == '/sbin/ldconfig':
                    pkg = self.lines[0]
                    self.lines = []
                    self.lines.append('{0} -p /sbin/ldconfig'.format(pkg))
        return newline
