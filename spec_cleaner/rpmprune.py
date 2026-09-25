# vim: set ts=4 sw=4 et: coding=UTF-8

"""Cleanup classes that drop most of the content."""

from itertools import chain
from typing import IO

from .rpmsection import Section


class RpmClean(Section):
    """Remove clean section."""

    codeblocks: int = 0

    def _check_conditions(self, line: str) -> None:
        """Track real conditionals, and count comment markers opened in the dropped body."""
        if self.reg.re_if.match(line):
            self._condition_counter += 1
        elif self.reg.re_endif.match(line):
            self._condition_counter -= 1
        elif self.reg.re_codeblock.match(line):
            self.codeblocks += 1
        elif self.codeblocks and self.reg.re_endcodeblock.match(line):
            self.codeblocks -= 1
        self.condition = self._condition_counter > 0

    def output(self, fout: IO[str], newline: bool = True, new_class_name: str = '') -> None:
        """Output only the open conditions and trailing comments, they belong to the next section."""
        opened: list[list[str]] = []
        comments: list[str] = []
        for line in self.lines:
            if self.reg.re_if.match(line):
                opened.append([line])
            elif opened and self.reg.re_else_elif.match(line):
                opened[-1].append(line)
            elif opened and self.reg.re_endif.match(line):
                opened.pop()
            if line.startswith('#') and not (
                self.reg.re_codeblock.match(line) or self.reg.re_endcodeblock.match(line)
            ):
                comments.append(line)
            else:
                comments = []
        # a blank line or the end of the file separates the comments from what follows
        if new_class_name in ('', 'Section'):
            comments = []
        for line in chain(*opened, comments):
            fout.write(line + '\n')


class RpmChangelog(Section):
    """Remove changelog entries."""

    def add(self, line: str) -> None:
        """
        Only add the first line of changelog.

        This translates to adding just %changelog.
        """
        # track conditions so their %else/%endif are dropped along with the %if
        self._check_conditions(line)
        if len(self.lines) == 0:
            Section.add(self, '%changelog')
