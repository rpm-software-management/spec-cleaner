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
        intact and only the 'make' word itself is replaced. A line led
        by assignments at its start is not rewritten when it joins
        commands with ';', '&' or '|': we cannot tell where the 'make'
        call ends there. Assignments after a separator
        ('cd tests && CFLAGS="-O2" make ...') are rewritten instead:
        the make call follows the separator, so the first-call-wins
        rule applies as for a plain midline make call.

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
            line = self.reg.re_make.sub(r'\1%make_build\3', line)
        elif env_safe and self.reg.re_make_env.match(line):
            line = self.reg.re_make_env.sub(r'\1%make_build\2', line)
        # remove the options that are part of %make_build macro, but only
        # from the arguments after it: the leading assignments (group 1)
        # are kept verbatim
        match = self.reg.re_make_build.match(line)
        if match is None and env_safe:
            match = self.reg.re_make_build_env.match(line)
        if match:
            # the arguments are the last group of either pattern: group 3
            # of re_make_build and group 2 of re_make_build_env; every
            # group participates, so lastindex is always set
            lastindex = match.lastindex
            assert lastindex is not None
            args = self._strip_make_args(match.group(lastindex))
            line = match.group(1) + '%make_build' + args
        return line

    def _strip_make_args(self, args: str) -> str:
        """
        Strip %make_build-covered flags from the matched make call only.

        Flag cleanup stops at the next real shell command boundary, so
        an assignment belonging to a later command ('make check;
        V=1 ./verify') is preserved verbatim. A boundary inside quotes
        or after a backslash is not a boundary.

        Args:
            args: The arguments after the %make_build macro.

        Return:
            The arguments with flags stripped up to the first boundary.
        """
        boundary = self._first_shell_separator(args)
        if boundary is None:
            head, tail = args, ''
        else:
            head, tail = args[:boundary], args[boundary:]
        # remove smp flags (with all preceding whitespace, not just one space)
        head = self.reg.re_smp_mflags_ws.sub('', head)
        # remove verbosity (with all preceding whitespace)
        head = self.reg.re_verbose_ws.sub('', head)
        head = self.reg.re_verbose_long_ws.sub('', head)
        return head + tail

    @staticmethod
    def _first_shell_separator(line: str) -> int | None:
        """
        Index of the first unquoted, unescaped ';', '&' or '|'.

        Args:
            line: A string representing a line to process.

        Return:
            The index of the first real shell command boundary, or None.
        """
        quote = None
        escaped = False
        for index, char in enumerate(line):
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
                return index
        return None

    @staticmethod
    def _has_shell_separator(line: str) -> bool:
        """
        Check whether the line joins shell commands outside of quotes.

        Args:
            line: A string representing a line to process.

        Return:
            True if the line contains an unquoted ';', '&' or '|'.
        """
        return RpmCheck._first_shell_separator(line) is not None
