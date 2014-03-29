# vim: set ts=4 sw=4 et: coding=UTF-8

from rpmsection import Section


class RpmBuild(Section):
    """
        Replace various troublemakers in build phase
    """

    def add(self, line):
        line = self._complete_cleanup(line)

        # smp_mflags for jobs
        if not self.reg.re_comment.match(line):
            line = self.embrace_macros(line)
        line = self.reg.re_jobs.sub('%{?_smp_mflags}', line)

        # add jobs if we have just make call on line
        # if user want single thread he should specify -j1
        if line.startswith('make'):
            # if there are no smp_flags or jobs spec just append it
            if line.find('%{?_smp_mflags}') == -1 and line.find('-j') == -1:
                # if the line ends with backslash, it continues on the next one,
                # so we can't just append, because we'll break the formatting
                if line.endswith('\\'):
                    line = '{0} {1} \\'.format(line[:-1], '%{?_smp_mflags}')
                else:
                    line = '{0} {1}'.format(line, '%{?_smp_mflags}')

        # if user uses cmake directly just recommend him using the macros
        if line.startswith('cmake'):
            self.lines.append('# FIXME: you should use %cmake macros')

        Section.add(self, line)
