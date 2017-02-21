# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section

import re, shlex, getopt

class RpmScriptlets(Section):

    '''
        Do %post -p /sbin/ldconfig when only scriplet command is /sbin/ldconfig
    '''

    re_update_alt = re.compile(r'^\s*(%\{_sbindir\}/)?update-alternatives')

    def __init__(self, options):
        Section.__init__(self, options)
        self.alt_continued = False

    def add(self, line):
        line = self._complete_cleanup(line)
        if self.re_update_alt.match(line):
            if line[-1] == "\\":
                self.alt_continued = True
        elif self.alt_continued:
            if line[-1] != "\\":
                self.alt_continued = False
        else:
            Section.add(self, line)

    def output(self, fout, newline=True, new_class=None):
        if not self.minimal:
            self._collapse_multiline_ldconfig()

        open_if = "if [ $1 -eq 0 ] ; then"
        close_if = "fi"
        if open_if in self.lines and close_if in self.lines and \
            self.lines.index(open_if) + 1 == self.lines.index(close_if):
                i = self.lines.index(open_if)
                del self.lines[i:i+2]

        if not self._is_empty():
            Section.output(self, fout, newline, new_class)

    def _is_empty(self):
        if len([l for l in self.lines if l]) > 1:
            return False
        opts, args = getopt.getopt(shlex.split(self.lines[0])[1:], "n:p:f:")
        optdict = dict(opts)
        if "-p" in optdict and optdict["-p"]:
            return False
        if "-f" in optdict and optdict["-f"]:
            return False
        return True

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
