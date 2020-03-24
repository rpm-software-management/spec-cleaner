# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmpreamble import RpmPreamble
from .rpmsection import Section


class RpmPackage(RpmPreamble):
    """
    A class providing methods for %package section cleaning.

    We handle subpackage case as the normal preamble.
    """

    def add(self, line: str) -> None:
        # The first line (%package) should always be added and is different
        # from the lines we handle in RpmPreamble.
        if not self.previous_line:
            Section.add(self, line)
            return

        # If the package is lang package we add here comment about the lang
        # package
        if (
            len(self.lines) == 1
            and (
                self.previous_line.startswith('%')
                and (self.previous_line.endswith(' lang') or self.previous_line.endswith('-lang'))
            )
            and not line.startswith('#')
        ):
            if not self.minimal:
                Section.add(self, '# FIXME: consider using %%lang_package macro')

        RpmPreamble.add(self, line)
