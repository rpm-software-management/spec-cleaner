# vim: set ts=4 sw=4 et: coding=UTF-8

import re
import os
import time

from rpmsection import Section


class RpmCopyright(Section):
    """
    Class that always creates default SUSE copyright.
    Keeps around Copyrights of other uses and some of the build defines
    that are still relevant. Everything else is ignored.
    """

    re_copyright = re.compile('^#\s*Copyright\ \(c\)\s*', re.IGNORECASE)
    re_suse_copyright = re.compile('SUSE LINUX Products GmbH, Nuernberg, Germany.\s*$', re.IGNORECASE)
    re_rootforbuild = re.compile('^#\s*needsrootforbuild\s*$', re.IGNORECASE)
    re_binariesforbuld = re.compile('^#\s*needsbinariesforbuild\s*$', re.IGNORECASE)
    re_nodebuginfo = re.compile('^#\s*nodebuginfo\s*$', re.IGNORECASE)
    re_icecream = re.compile('^#\s*icecream\s*$', re.IGNORECASE)

    copyrights = []
    buildrules = []


    def __init__(self, re_unbrace_keywords, spec):
        Section.__init__(self, re_unbrace_keywords)
        self.spec = spec


    def _add_pkg_header(self):
        specname = os.path.splitext(os.path.basename(self.spec))[0]
        self.lines.append('''#
# spec file for package {0}
#'''.format(specname))


    def _create_default_copyright(self):
        year = time.strftime('%Y', time.localtime(time.time()))
        return '# Copyright (c) {0} SUSE LINUX Products GmbH, Nuernberg, Germany.'.format(year)


    def _add_copyright(self):
        copyright = self._create_default_copyright()
        self.lines.append(copyright)

        for i in self.copyrights:
            self.lines.append(i)


    def _add_default_license(self):
        self.lines.append('''#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#''')


    def _add_buildrules(self):
        for i in sorted(self.buildrules):
            self.lines.append(i)


    def add(self, line):
        if not self.lines and not line:
            return
        if self.re_copyright.match(line) and not self.re_suse_copyright.search(line):
            self.copyrights.append(line)
        elif self.re_rootforbuild.match(line):
            self.buildrules.append('# needsrootforbuild')
        elif self.re_binariesforbuld.match(line):
            self.buildrules.append('# needsbinariesforbuild')
        elif self.re_nodebuginfo.match(line):
            self.buildrules.append('# nodebuginfo')
        elif self.re_icecream.match(line):
            self.buildrules.append('# icecream')
        else:
            # anything not in our rules gets tossed out
            return


    def output(self, fout):
        self._add_pkg_header()
        self._add_copyright()
        self._add_default_license()
        self._add_buildrules()
        # trailing enter
        self.lines.append("")
        Section.output(self, fout)
