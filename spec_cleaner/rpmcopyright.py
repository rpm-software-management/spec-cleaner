# vim: set ts=4 sw=4 et: coding=UTF-8

import os
from typing import IO

from .rpmsection import Section


class RpmCopyright(Section):
    """
    A class providing methods for copyright section cleaning.

    It always creates default SUSE copyright.
    Keeps around Copyrights of other uses and some of the build defines
    that are still relevant. Everything else is ignored.
    """

    def __init__(self, options):
        """Initialize default variables."""
        Section.__init__(self, options)
        self.no_copyright = options['no_copyright']
        self.year = options['copyright_year']
        self.copyrights = []
        self.buildrules = []
        self.distro_copyright = '# Copyright (c) {0} SUSE LLC'.format(self.year)
        self.vimmodeline = ''

    def _add_pkg_header(self):
        """Add specfile name to the Copyright section."""
        specname = os.path.splitext(os.path.basename(self.spec))[0]
        self.lines.append(
            """#
# spec file for package {0}
#""".format(
                specname
            )
        )

    def _add_copyright(self):
        """Add SUSE copyright information to the Copyright section."""
        self.lines.append(self.distro_copyright)

        for i in self.copyrights:
            self.lines.append(i)

    def _add_default_license(self):
        """Add default license text to the Copyright section."""
        self.lines.append(
            """#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#"""
        )

    def _add_buildrules(self) -> None:
        """Add buildrules."""
        for i in sorted(self.buildrules):
            self.lines.append(i)

    def _add_modelines(self) -> None:
        """Add vim modeline if found."""
        if self.vimmodeline:
            self.lines.append(self.vimmodeline)

    def add(self, line: str) -> None:
        """Run the cleanup of the line.

        If we have no copyright header we actually should not touch it not
        wipe out, thus just add everything to known lines
        """
        if self.no_copyright:
            self.lines.append(line)
            return
        if not self.lines and not line:
            return
        copyright_match = self.reg.re_copyright_string.match(line)
        if copyright_match and not self.reg.re_suse_copyright.search(line):
            # always replace whitespace garbage on copyright line
            line = '# Copyright (c) {0}'.format(copyright_match.group(1))
            self.copyrights.append(line)
        elif self.reg.re_rootforbuild.match(line):
            self.buildrules.append('# needsrootforbuild')
        elif self.reg.re_binariesforbuild.match(line):
            self.buildrules.append('# needsbinariesforbuild')
        elif self.reg.re_nodebuginfo.match(line):
            self.buildrules.append('# nodebuginfo')
        elif self.reg.re_icecream.match(line):
            self.buildrules.append('# icecream')
        elif self.reg.re_vimmodeline.match(line):
            self.vimmodeline = line
        elif self.reg.re_sslcerts.match(line):
            self.buildrules.append('# needssslcertforbuild')
        else:
            # anything not in our rules gets tossed out
            return

    def output(self, fout: IO[str], newline: bool = True, new_class_name: str = ''):
        """Manage printing of the Copyright section."""
        if not self.no_copyright:
            self._add_modelines()
            self._add_pkg_header()
            self._add_copyright()
            self._add_default_license()
            self._add_buildrules()
            self.lines.append('')
            self.lines.append('')
        else:
            newline = False
        Section.output(self, fout, newline, new_class_name)
