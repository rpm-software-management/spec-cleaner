# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmCheck(Section):
    """
    A class providing methods for %check section cleaning.

    Replace various troublemakers in check phase.
    """

    shell_section = True

    def add(self, line: str) -> None:
        """Process one line of the %check section."""
        line = self._complete_cleanup(line)

        # smp_mflags for jobs macro replacement
        line = self.reg.re_jobs.sub('%{?_smp_mflags}', line)

        if not self.minimal:
            line = self._replace_pytest(line)
            line = self._replace_unittest(line)
            line = self._replace_make(line)

        Section.add_cleaned(self, line)

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

        The call may be led by shell variable assignments, e.g.
        'CFLAGS="%{optflags}" make V=1 ...'; the assignments are kept
        intact and only the 'make' word itself is replaced. Lines that
        join commands with ';', '&' or '|' are not rewritten when led
        by assignments: we cannot tell where the 'make' call ends there.

        Args:
            line: A string representing a line to process.

        Return:
            The processed line.
        """
        # if it is comment line then do nothing
        if line.lstrip().startswith('#'):
            return line
        # find all make calls and replace them with %make_build
        env_safe = not self._has_shell_separator(line)
        if self.reg.re_make.match(line):
            line = self.reg.re_make.sub(r'\1%make_build\2', line)
        elif env_safe and self.reg.re_make_env.match(line):
            line = self.reg.re_make_env.sub(r'\1%make_build\2', line)
        # remove the options that are part of %make_build macro, but only
        # from the arguments after it: the leading assignments (group 1)
        # are kept verbatim
        match = self.reg.re_make_build.match(line)
        if match is None and env_safe:
            match = self.reg.re_make_build_env.match(line)
        if match:
            args = match.group(2)
            # remove smp flags (with all preceding whitespace, not just one space)
            args = self.reg.re_smp_mflags_ws.sub('', args)
            # remove verbosity (with all preceding whitespace)
            args = self.reg.re_verbose_ws.sub('', args)
            args = self.reg.re_verbose_long_ws.sub('', args)
            line = match.group(1) + '%make_build' + args
        return line

    @staticmethod
    def _has_shell_separator(line: str) -> bool:
        """
        Check whether the line joins shell commands outside of quotes.

        Args:
            line: A string representing a line to process.

        Return:
            True if the line contains an unquoted ';', '&' or '|'.
        """
        quote = None
        escaped = False
        for char in line:
            if escaped:
                escaped = False
            elif char == '\\' and quote != "'":
                escaped = True
            elif quote:
                if char == quote:
                    quote = None
            elif char in ('"', "'"):
                quote = char
            elif char in (';', '&', '|'):
                return True
        return False
