# vim: set ts=4 sw=4 et: coding=UTF-8

from pathlib import Path

from .rpmsection import Section


class RpmFiles(Section):
    """A class providing methods for %files section cleaning."""

    def add(self, line: str) -> None:
        line = self._complete_cleanup(line)
        line = self.strip_useless_spaces(line)
        line = self._remove_doc_on_man(line)
        line = self._move_license_from_doc(line)
        line = self._expand_python_sitelib(line)
        # we only get empty %doc left over
        if line == '%doc ':
            return

        if not self.minimal:
            # prune obsolete defattr that is default
            if self.reg.re_defattr.match(line):
                return
            line = self._set_man_compression(line)

        # toss out empty lines if there are more than one in succession
        if line == '' and (not self.previous_line or self.previous_line == ''):
            return

        Section.add(self, line)

    @staticmethod
    def _remove_doc_on_man(line: str) -> str:
        """
        Remove all "%doc %_mandir" to -> "%_mandir" as it is pointless to do twice.

        Args:
            line: A string representing a line to process.

        Returns:
            The processed line.
        """
        line = line.replace('%doc %{_mandir}', '%{_mandir}', 1)
        line = line.replace('%doc %{_infodir}', '%{_infodir}', 1)
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
        if line.startswith('%doc') and self.reg.re_doclicense.search(line):
            licences = ''
            match = self.reg.re_doclicense.search(line)
            while match:
                licences += match.group()
                line = self.reg.re_doclicense.sub('', line, 1)
                match = self.reg.re_doclicense.search(line)
            Section.add(self, '%license {}'.format(licences))
        return line

    def _expand_python_sitelib(self, line: str) -> str:
        """
        Replaces the usage of "%{python_sitelib}/*" with a more
        specific line that includes the package name:

            %{python_sitelib}/packagename
            %{python_sitelib}/packagename-%{version}*-info

        This function uses the package name and removes the "python-"
        prefix if it exists, so the name is the python module name.
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
                name = name[0:-len('.spec')]
                # remove python prefix if exists
                if name.startswith('python-'):
                    name = name[len('python-'):]

            macro = match.group('macro')
            line = (f'{macro}/{name}\n'
                    f'{macro}/{name}-%{{version}}*-info')

        return line
