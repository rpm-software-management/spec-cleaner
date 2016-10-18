# vim: set ts=4 sw=4 et: coding=UTF-8

# We basically extend rpmcheck
from .rpmcheck import RpmCheck


class RpmBuild(RpmCheck):

    """
        Replace various troublemakers in build phase
    """

    def add(self, line):
        # we do not want to run suseupdateconfig, deprecated
        if self.reg.re_suseupdateconfig.search(line):
            return

        # if user uses cmake/configure directly just recommend him using the macros
        # but check on the multiline entry and do not ammend that
        if not self.minimal:
            if (not self.previous_line \
               or (not self.previous_line.startswith('#') \
               and not self.previous_line.endswith('\\'))) \
               and self.reg.re_configure.match(line):
                self.lines.append('# FIXME: you should use the %%configure macro')
            if (not self.previous_line \
               or (not self.previous_line.startswith('#') \
               and not self.previous_line.endswith('\\'))) \
               and self.reg.re_cmake.match(line):
                self.lines.append('# FIXME: you should use %%cmake macros')

        RpmCheck.add(self, line)
