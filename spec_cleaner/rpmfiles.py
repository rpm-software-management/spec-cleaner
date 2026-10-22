# vim: set ts=4 sw=4 et: coding=UTF-8

from pathlib import Path

from .rpmsection import Section


class RpmFiles(Section):
    """A class providing methods for %files section cleaning."""

    _defattr_seen: bool = False

    def add(self, line: str) -> None:
        """Process one line of the %files section."""
        line = self._complete_cleanup(line)
        line = self.strip_useless_spaces(line)

        if not self.minimal:
            # The %doc rewrites change what the built package flags: man/info
            # pages lose their prefix and licence files move to %license.
            # The minimal run only formats, so it keeps the markers as written.
            line = self._remove_doc_on_man(line)
            line = self._move_license_from_doc(line)
            # we only get empty %doc left over
            if line == '%doc ':
                return
            # prune obsolete defattr that is default, unless it resets an earlier one;
            # a resumed body cannot tell whether one came before the conditional
            if line.startswith('%defattr'):
                if self.reg.re_defattr.match(line) and not self._defattr_seen and not self.headless:
                    return
                self._defattr_seen = True
            line = self._set_man_compression(line)
            line = self._expand_python_sitelib(line)

        # toss out empty lines if there are more than one in succession
        if line == '' and (not self.previous_line or self.previous_line == ''):
            return

        # cleaned twice on purpose: the transforms above re-dirty the line
        Section.add(self, line)

    @staticmethod
    def _remove_doc_on_man(line: str) -> str:
        """
        Remove the "%doc" prefix from lines listing only man/info pages.

        rpm flags everything below %{_mandir} and %{_infodir} as
        documentation on its own, so the prefix states nothing there.
        A line mixing man/info pages with other files keeps its prefix:
        the prefix still carries the documentation flag for those files.

        Args:
            line: A string representing a line to process.

        Returns:
            The processed line.
        """
        if not line.startswith('%doc '):
            return line
        files = line[len('%doc ') :].split()
        if files and all(
            file.startswith('%{_mandir}') or file.startswith('%{_infodir}') for file in files
        ):
            return line[len('%doc ') :]
        return line

    def _set_man_compression(self, line: str) -> str:
        """
        Set proper compression suffix on man/info pages.

        Instead of .gz/.* use the proper macro variable.

        Args:
           line: A string representing a line to process.

        Returns:
            The processed line.
        """
        if line.startswith('%{_mandir}'):
            line = self.reg.re_man_compression.sub(r'\1%{?ext_man}', line)
        if line.startswith('%{_infodir}'):
            line = self.reg.re_info_compression.sub('.info%{?ext_info}', line)
        return line

    def _move_license_from_doc(self, line: str) -> str:
        """
        Move license file from %doc to %license.

        Args:
           line: A string representing a line to process.

        Returns:
            The processed line.
        """
        # the qualifiers apply to every file on the line, so a split would lose them
        if (
            line.startswith('%doc')
            and self.reg.re_doclicense.search(line)
            and not self.reg.re_file_qualifier.search(line)
        ):
            licences = ''
            match = self.reg.re_doclicense.search(line)
            while match:
                licences += match.group()
                line = self.reg.re_doclicense.sub('', line, 1)
                match = self.reg.re_doclicense.search(line)
            Section.add(self, f'%license {licences}')
        return line

    def _expand_python_sitelib(self, line: str) -> str:
        """
        Replace the usage of "%{python_sitelib}/*" with package-specific lines.

        Replaces the usage of "%{python_sitelib}/*" with a more
        specific line that includes the package name:

            %{python_sitelib}/packagename
            %{python_sitelib}/packagename-%{version}*-info

        This function uses the package name, removes the "python-" (or
        "python3-", ...) prefix if it exists and replaces dashes with
        underscores, so the name is the python module name.
        """
        name = '%{name}'
        match = self.reg.re_python_sitelib_glob.match(line)
        if match:
            # try to use the python module name for the python sitelib
            # line, calculating the name from the spec file str.
            if self.spec:
                # remove full path
                name = Path(self.spec).name
                # remove .spec
                name = name[0 : -len('.spec')]
                # remove python prefix if exists
                prefix_match = self.reg.re_python_package_name.match(name)
                if prefix_match:
                    name = prefix_match.group(1)
                name = name.replace('-', '_')

            macro = match.group('macro')
            line = f'{macro}/{name}\n{macro}/{name}-%{{version}}*-info'

        return line
