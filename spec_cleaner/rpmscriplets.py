# vim: set ts=4 sw=4 et: coding=UTF-8

from rpmsection import Section


class RpmScriptlets(Section):
    '''
        Do %post -p /sbin/ldconfig when only scriplet command is /sbin/ldconfig
    '''

    def output(self, fout):
        # if we have 2 or 3 lines where last one is empty
        nolines = len(self.lines)
        if nolines == 2 or ( nolines == 3 and self.lines[2] == '') \
                and self.lines[1] == '/sbin/ldconfig':
            pkg = self.lines[0]
            self.lines = []
            self.lines.append('{0} -p /sbin/ldconfig'.format(pkg))
            self.lines.append('')
        Section.output(self, fout)
