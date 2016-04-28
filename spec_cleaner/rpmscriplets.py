# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmScriptlets(Section):

    '''
        Do %post -p /sbin/ldconfig when only scriplet command is /sbin/ldconfig
    '''

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
