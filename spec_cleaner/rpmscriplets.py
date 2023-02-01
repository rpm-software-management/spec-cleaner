# vim: set ts=4 sw=4 et: coding=UTF-8
from typing import IO

from .rpmsection import Section


class RpmScriptlets(Section):
    """
    A class providing methods for scriptlet section cleaning.

    Do %post -p /sbin/ldconfig when only scriplet command is /sbin/ldconfig.
    """

    def add(self, line: str) -> None:
        """Run the cleanup of the line."""
        line = self._complete_cleanup(line)
        line = self._remove_deprecated_ldconfig(line)
        Section.add(self, line)

    def _remove_deprecated_ldconfig(self, line: str) -> str:
        """
        Replace %run_ldconfig with /sbin/ldconfig.

        Args:
            line: A string representing a line to process.

        Returns:
            The processed line.
        """
        line = self.reg.re_ldconfig.sub('/sbin/ldconfig', line)
        return line

    def output(self, fout: IO[str], newline: bool = True, new_class_name: str = '') -> None:
        """Manage to print the section."""
        if not self.minimal:
            self._collapse_multiline_ldconfig()
        Section.output(self, fout, newline, new_class_name)

    def _collapse_multiline_ldconfig(self) -> None:
        """
        Merge two lines ldconfig call to the one line.

        Adjust lines member accordingly.
        """
        # if we have 2 lines or rest of them are empty, pop those
        for i in reversed(self.lines):
            if i:
                break
            else:
                self.lines.pop()
        if len(self.lines) == 2:
            if self.lines[1] == '/sbin/ldconfig':
                pkg = self.lines[0]
                self.lines = []
                self.lines.append('{0} -p /sbin/ldconfig'.format(pkg))
