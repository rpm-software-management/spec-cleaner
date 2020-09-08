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
            line = self._replace_pytest(line)
            line = self._replace_unittest(line)
            line = self._replace_make(line)

        Section.add(self, line)

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

    def _replace_unittest(self, line: str) -> str:
        """
        Replace various pytest calls with %pyunittest or %pyunittest_arch macros.

        Args:
            line: A string representing a line to process.

        Return:
            The processed line.
        """
        line = self.reg.re_pyunittest.sub('%pyunittest', line)
        line = self.reg.re_pyunittest_arch.sub('%pyunittest_arch', line)
        return line

    def _replace_make(self, line: str) -> str:
        """
        Replace 'make' call with '%make_build' macro.

        Args:
            line: A string representing a line to process.

        Return:
            The processed line.
        """
        # if it is comment line then do nothing
        if line.lstrip().startswith('#'):
            return line
        # find all make calls and replace them with %make_build
        if self.reg.re_make.match(line):
            line = self.reg.re_make.sub(r'\1%make_build\2', line)
        # remove from line all the options that are part of %make_build macro
        if self.reg.re_make_build.match(line):
            # remove smp flags
            line = line.replace(' %{?_smp_mflags}', '')
            # remove verbosity
            line = line.replace(' V=1', '')
            line = line.replace(' VERBOSE=1', '')
        return line
