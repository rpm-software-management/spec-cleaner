# vim: set ts=4 sw=4 et: coding=UTF-8

from .rpmsection import Section


class RpmPrep(Section):
    """
    A class providing methods for %prep section cleaning.

    It simplifies %setup and %patch lines.
    """

    shell_section = True

    def add(self, line):
        """Executes the format operations for the Prep phase."""
        line = self._complete_cleanup(line)
        line = self._cleanup_setup(line)
        if not self.minimal:
            line = self._prepare_patch(line)
            line = self._remove_dephell_call(line)
        Section.add(self, line)

    def _cleanup_setup(self, line: str) -> str:
        """
        Remove the useless stuff from %setup line.

        Args:
            line: A string representing a line to process.

        Return:
            The processed line.
        """
        # NOTE: not using regexp as this covers 99% cases for now
        if line.startswith('%setup'):
            # drop -q also from flag clusters like -qa1, it is re-added in front
            args = ['-' + arg[2:] if arg.startswith('-q') else arg for arg in line.split()]
            line = ' '.join(arg for arg in args if arg != '-')
            line = self.reg.re_setup.sub(' ', line)
            line = self.strip_useless_spaces(line)
            line = line.replace('%setup', '%setup -q')

        return line

    def _remove_dephell_call(self, line: str) -> str:
        """
        Replace direct dephell calls with macro call.

        Args:
            line: A string representing a line to process.

        Return:
            The processed line.
        """
        if self.reg.re_dephell_setup.match(line):
            line = '%dephell_gensetup'

        return line

    def _prepare_patch(self, line: str) -> str:
        """
        Convert patchlines to something pretty.

        E.g. it converts "%patch50 -p10" to "%patch -P 50 -p10" and so on.

        Args:
            line: A string representing a line to process.

        Return:
            The line with pretty patchlines.
        """
        # -p0 is default
        if line.startswith('%patch'):
            line = line.replace('-p0', '')
        # %patch without a patch number was %patch0 before, convert to %patch0 for the reges
        if (line.startswith('%patch ') or line == '%patch') and not self._has_patch_number(line):
            line = line.replace('%patch', '%patch0')

        # convert the %patch50 -p10 to %patch -P 50 -p10
        match = self.reg.re_patch_prep.match(line)
        if match:
            line = self.strip_useless_spaces(f'%patch -P {match.group(1)} {match.group(2)}')

        return line

    @staticmethod
    def _has_patch_number(line: str) -> bool:
        """
        Check whether a %patch line names its patch by -P or as a positional argument.

        Args:
            line: A string representing a line to process.

        Return:
            True if the patch number is given, False otherwise.
        """
        args = iter(line.split()[1:])
        for arg in args:
            if arg.startswith('-P'):
                return True
            if arg in ('-p', '-b', '-z', '-F', '-d', '-o'):
                # the option value is not a patch number
                next(args, None)
            elif not arg.startswith('-'):
                return True
        return False
