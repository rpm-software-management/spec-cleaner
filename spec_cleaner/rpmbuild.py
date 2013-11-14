# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from rpmsection import Section


class RpmBuild(Section):
    """
        Replace %{?jobs:-j%jobs} (suse-ism) with %{?_smp_mflags}
    """

    re_jobs = re.compile('%{(_smp_mflags|\?jobs:\s*-j\s*%(jobs|{jobs}))}')
    re_comment = re.compile('^$|^\s*#')

    def add(self, line):
        if not self.re_comment.match(line):
            line = embrace_macros(line)
        line = self.re_jobs.sub('%{?_smp_mflags}', line)

        Section.add(self, line)
