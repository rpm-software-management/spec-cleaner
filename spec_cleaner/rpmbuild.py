# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section


class RpmBuild(Section):
    """
        Replace %{?jobs:-j%jobs} (suse-ism) with %{?_smp_mflags}
    """

    def add(self, line):
        if not self.reg.re_comment.match(line):
            line = self.embrace_macros(line)
        line = self.reg.re_jobs.sub('%{?_smp_mflags}', line)

        Section.add(self, line)
