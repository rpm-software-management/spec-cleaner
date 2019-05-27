# vim: set ts=4 sw=4 et: coding=UTF-8

# We basically extend rpmcheck
from .rpmcheck import RpmCheck


class RpmBuild(RpmCheck):

    """
    A class providing methods for %build section cleaning.
    """

    def add(self, line: str) -> None:
        # we do not want to run suseupdateconfig, deprecated
        if self.reg.re_suseupdateconfig.search(line):
            return

        # if user uses cmake/configure directly just recommend him using the macros
        if not self.minimal:
            self._comment_macro_calls(line)

        RpmCheck.add(self, line)

    def _comment_macro_calls(self, line: str) -> None:
        """
        Add a comment if the package uses direct call of certain build tools instead of macro.

        Args:
            line: A string representing a line to process.
        """
        if self.reg.re_configure.match(line):
            msg = '# FIXME: you should use the %%configure macro'
        elif self.reg.re_cmake.match(line):
            msg = '# FIXME: you should use %%cmake macros'
        elif self.reg.re_meson.match(line):
            msg = '# FIXME: you should use %%meson macros'
        elif self.reg.re_qmake5.match(line):
            msg = '# FIXME: you should use %qmake5 macro'
        else:
            return

        position = len(self.lines)
        if self.previous_line and self.previous_line.endswith('\\'):
            # Backtrack until we are on top of multiline command
            for i in reversed(self.lines):
                if i.endswith('\\'):
                    position -= 1
                else:
                    # we stop backtracking on the first
                    # non-backslashed line
                    break
        # Check if on the position above is no comment
        # if not add our message
        if not self.lines[position - 1].startswith('#'):
            self.lines.insert(position, msg)
