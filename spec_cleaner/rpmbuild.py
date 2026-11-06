# vim: set ts=4 sw=4 et: coding=UTF-8

import re

# We basically extend rpmcheck
from .rpmcheck import RpmCheck


class RpmBuild(RpmCheck):
    """A class providing methods for %build section cleaning."""

    def add(self, line: str) -> None:
        """Process one line of the %build section."""
        # we do not want to run suseupdateconfig, deprecated
        if self.reg.re_suseupdateconfig.search(line):
            return

        # if user uses cmake/configure directly just recommend him using the macros
        if not self.minimal:
            self._comment_macro_calls(line)

        RpmCheck.add(self, line)

    def _comment_macro_calls(self, line: str) -> None:
        """
        Add a comment if the package uses direct call of build tools instead of macro.

        Args:
            line: A string representing a line to process.
        """
        # if the line itself is comment then we do not add any fixme on top of them
        if self.reg.re_comment.match(line):
            return
        # An echo command never invokes a build tool, and a tool word
        # inside quotes is prose, not an invocation: check each shell
        # command on its own, skipping echo-led segments, so 'echo foo;
        # echo cmake' stays quiet while 'echo done; cmake .' still
        # gets flagged. The tool order is the old whole-line order, so
        # a line mixing tools keeps its previous message.
        segments = [
            segment
            for segment in self._split_shell_commands(line)
            if not re.match(r'\s*echo(\s|$)', segment)
        ]
        match_segments = [
            ''.join(text for text, quoted in self._split_quoted(segment) if not quoted)
            for segment in segments
        ]
        # otherwise process the fixes
        msg = None
        for pattern, message in (
            (self.reg.re_configure, '# FIXME: you should use the %%configure macro'),
            (self.reg.re_cmake, '# FIXME: you should use the %%cmake macros'),
            (self.reg.re_meson, '# FIXME: you should use the %%meson macros'),
            (self.reg.re_qmake5, '# FIXME: you should use the %%qmake5 macro'),
        ):
            if any(pattern.match(segment) for segment in match_segments):
                msg = message
                break
        if msg is None:
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
        # a body resumed after a conditional end has the line above it in previous_line
        above = self.lines[position - 1] if position else self.previous_line
        if not (above and above.startswith('#')):
            self.lines.insert(position, msg)
