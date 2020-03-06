# vim: set ts=4 sw=4 et: coding=UTF-8
from typing import Any, Dict

from .rpmsection import Section


class RpmDescription(Section):
    """
    A class providing methods for %description section cleaning.

    Only keep one empty line for many consecutive ones.
    Remove Authors from description.
    """

    def __init__(self, options: Dict[str, Any]) -> None:
        Section.__init__(self, options)
        self.removing_authors = False
        # Tracks the use of a macro. When this happens and we're still in a
        # description, we actually don't know where we are so we just put all
        # the following lines blindly, without trying to fix anything.
        self.unknown_line = False

    def add(self, line: str) -> None:
        if self.previous_line and len(line) > 0 and line[0] == '%':
            self.unknown_line = True

        if self.removing_authors and not self.unknown_line:
            return

        if len(line) == 0:
            if not self.previous_line or len(self.previous_line) == 0:
                return

        if self.reg.re_authors.match(line) and not self.minimal:
            self.removing_authors = True
            return

        Section.add(self, line)
