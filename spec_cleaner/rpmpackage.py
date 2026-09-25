# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmpreamble import RpmPreamble
from .rpmsection import Section


class RpmPackage(RpmPreamble):
    """
    A class providing methods for %package section cleaning.

    We handle subpackage case as the normal preamble.
    """

    def __init__(self, options):
        """Initialize the subpackage preamble."""
        RpmPreamble.__init__(self, options)
        # -lang packages whose supplements key on this subpackage, from its %package -n name
        self._lang_package = set()
        self.paragraph.lang_package = self._lang_package

    def start_subparagraph(self):
        """Start a nested paragraph, pruning only this subpackage's -lang Recommends."""
        RpmPreamble.start_subparagraph(self)
        self.paragraph.lang_package = self._lang_package

    def add(self, line: str) -> None:
        """Process one line of the %package section."""
        # The first line (%package) should always be added and is different
        # from the lines we handle in RpmPreamble.
        # keep_space stores empty lines as '', so only None marks the first line.
        if self.previous_line is None:
            Section.add(self, line)
            match = self.reg.re_lang_package_name.search(line)
            if match:
                name = self.reg.re_macro_spelling.sub(r'%{\1}', match.group(1))
                self._lang_package = self.options['lang_package'] & {f'{name}-lang'}
                self.paragraph.lang_package = self._lang_package
            return

        # If the package is lang package we add here comment about the lang
        # package, unless the %lang_package macro is already used (#273)
        if (
            len(self.lines) == 1
            and (
                self.previous_line.startswith('%')
                and (self.previous_line.endswith(' lang') or self.previous_line.endswith('-lang'))
            )
            and not line.startswith('#')
            and not self.options.get('lang_package', False)
        ):
            if not self.minimal:
                Section.add(self, '# FIXME: consider using %%lang_package macro')

        RpmPreamble.add(self, line)
