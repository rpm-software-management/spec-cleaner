# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmCheck(Section):

    """
    A class providing methods for %check section cleaning.

    Replace various troublemakers in check phase.
    """

    def add(self, line: str) -> None:
        line = self._complete_cleanup(line)

        # smp_mflags for jobs macro replacement
        line = self.reg.re_jobs.sub('%{?_smp_mflags}', line)

        if not self.minimal:
            line = self._add_jobs(line)
            line = self._replace_pytest(line)

        Section.add(self, line)

    def _add_jobs(self, line: str) -> str:
        """
        Add %{?_smp_mflags} to 'make' call.

        Args:
            line: A string representing a line to process.

        Return:
            The processed line.
        """
        # add jobs if we have just make call on line
        # if user want single thread he should specify -j1
        if self.reg.re_make.match(line):
            # if there are no smp_flags or jobs spec
            if line.find('%{?_smp_mflags}') == -1 and line.find('-j') == -1:
                # Don't append %_smp_mflags if the line ends with a backslash,
                # it would break the formatting
                if not line.endswith('\\') and not line.lstrip().startswith('#'):
                    line = self.reg.re_make.sub(r'\1make %{?_smp_mflags}\2', line)
        return line

    def _replace_pytest(self, line: str) -> str:
        """
        Replace various pytest calls with %pytest or %pytest_arch macros.

        Args:
            line: A string representing a line to process.

        Return:
            The processed line.
        """
        line = self.reg.re_pytest.sub('%pytest', line)
        line = self.reg.re_pytest_arch.sub('%pytest_arch', line)
        return line
