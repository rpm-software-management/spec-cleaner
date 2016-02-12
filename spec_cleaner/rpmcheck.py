# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmCheck(Section):

    """
        Replace various troublemakers in check phase
    """

    def add(self, line):
        line = self._complete_cleanup(line)

        # smp_mflags for jobs
        if not self.reg.re_comment.match(line) and \
           not self.minimal:
            line = self.embrace_macros(line)
        line = self.reg.re_jobs.sub('%{?_smp_mflags}', line)

        # add jobs if we have just make call on line
        # if user want single thread he should specify -j1
        if not self.minimal and line.startswith('make'):
            # if there are no smp_flags or jobs spec
            if line.find('%{?_smp_mflags}') == -1 and line.find('-j') == -1:
                # Don't append %_smp_mflags if the line ends with a backslash,
                # it would break the formatting
                if not line.endswith('\\'):
                    line = self.reg.re_make.sub(r'\1make %{?_smp_mflags}\3', line)

        Section.add(self, line)
