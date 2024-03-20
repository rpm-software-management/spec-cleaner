# vim: set ts=4 sw=4 et: coding=UTF-8
from typing import IO, Any, Dict, List, Optional

from .rpmregexp import Regexp


class Section(object):
    """
    Basic object for parsing each section of spec file.

    It stores the lines in a list and remembers content of
    previous line at hand.
    The unbrace_keywords content is passed from creating
    object to reduce calculation price.
    Various functions do replacement of common typos to
    unify all the content.

    Attributes:
        lines: A list of all lines of the section.
        previous_line: A string that represents the previous line.
        spec: A string with the path to the processed specfile.
        minimal: A flag indicating whether we run in minimal mode (no intrusive operations).
        no_curlification: A flag indicating whether we want to convert variables to curly brackets.
        reg: A Regexp object that holds all regexps that will be used in spec-cleaner.
        condition: A flag representing if we are in the conditional or not.
        _condition_counter: An int for counting in how many (nested) condition we currently are.
    """

    def __init__(self, options: Dict[str, Any]) -> None:
        """Initialize variables."""
        self.lines: List[str] = []
        self.previous_line: Optional[str] = None
        self.spec: str = options['specfile']
        self.minimal: bool = options['minimal']
        self.no_curlification: bool = options['no_curlification']
        self.reg: Regexp = options['reg']
        # Are we inside of conditional or not
        self.condition: bool = False
        self._condition_counter: int = 0

    def _complete_cleanup(self, line: str) -> str:
        """
        Call all the cleanups in proper order.

        Therefore it can be called beforehand if we override add phase and want to do
        our replaces after cleanup.

        Args:
            line: A string representing a line to process.

        Returns:
            The cleaned line.
        """
        line = line.rstrip()
        # remove nbsp for normal spaces
        line = line.replace(u'\xa0', ' ')

        if not line.startswith('#'):
            is_python_module = self.reg.re_python_module.match(line)
            if (not self.minimal
                    and not self.no_curlification
                    # Do not embrace macros inside python_module
                    # gh#rpm-software-management/spec-cleaner#321
                    and not is_python_module):
                line = self.embrace_macros(line)
            line = self.replace_buildroot(line)
            line = self.replace_optflags(line)
            line = self.replace_known_dirs(line)
            line = self.replace_utils(line)
            line = self.replace_buildservice(line)
            line = self.replace_preamble_macros(line)
            line = self.replace_python_expand(line)

        return line

    def _check_conditions(self, line: str) -> None:
        """
        Set 'condition' member to True if we are in condition that is contained (False otherwise).

        Also adjusts '_condition_counter' member according to the fact whether we enter or leave the condition.

        Args:
            line: A string representing a line to process.
        """
        if self.reg.re_if.match(line) or self.reg.re_codeblock.match(line):
            self._condition_counter += 1
        if self.reg.re_endif.match(line) or self.reg.re_endcodeblock.match(line):
            self._condition_counter -= 1

        if self._condition_counter > 0:
            self.condition = True
        else:
            self.condition = False

    def add(self, line: str) -> None:
        """
        Run the cleanup of the line and add the line to the list of lines.

        Args:
            line: A string representing a line to process.
        """
        line = self._complete_cleanup(line)

        # conditions detect
        self._check_conditions(line)

        # append to the file
        self.lines.append(line)
        self.previous_line = line

    def output(self, fout: IO[str], newline: bool = True, new_class_name: str = '') -> None:
        """
        Manage printing of the section.

        Always append one empty line at the end if it is not present and a changelog is a trailing part of our spec
        so do not put nothing bellow. Also if we are jumping away just after writing one macroed line.

        Args:
            fout: A file object representing the output file.
            newline: A flag indicating whether we want to add a newline.
            new_class_name: A string with the Section name.
        """
        # we don't want to create new line
        if newline and len(self.lines) >= 1:
            if (
                self.lines[-1] != ''
                and self.lines[-1] != '%changelog'
                and not self.lines[-1].startswith('%if')
                and not self.lines[-1].startswith('%pre')
                and not self.lines[-1].startswith('%post')
                and not self.lines[-1].endswith('\\')
            ):
                self.lines.append('')
            if new_class_name != 'RpmScriptlets' and (
                self.lines[-1].startswith('%pre') or self.lines[-1].startswith('%post')
            ):
                self.lines.append('')
            # remove the newlines around ifs if they are not wanted
            if len(self.lines) >= 2:
                if self.lines[-1] == '' and (
                    self.lines[-2].startswith('%if') or self.lines[-2].startswith('%else')
                ):
                    self.lines.pop()

        for line in self.lines:
            fout.write(line + '\n')

    @staticmethod
    def strip_useless_spaces(line: str) -> str:
        """
        Remove useless multiple spaces in some areas.

        It can't be called everywhere so we have to call it in
        children classes where fit.

        Args:
            line: A string representing a line to process.

        Returns:
            The line without useless spaces.
        """
        return ' '.join(line.split())

    def embrace_macros(self, line: str) -> str:
        """
        Add {} around known macros that have no arguments and are not on whitelist.

        Whitelist is passed from caller object.

        Args:
            line: A string representing a line to process.

        Returns:
            The line with curlified macros.
        """
        # I don't think that this can be done within one regexp replacement
        # if you have idea, send me a patch :)

        # work only with non-commented part
        sp = line.split('#')
        # so, for now, put braces around everything, what looks like macro,
        previous = sp[0]

        while True:
            sp[0] = self.reg.re_macro.sub(r'\1%{\3}\5', sp[0])
            if sp[0] == previous:
                break
            else:
                previous = sp[0]

        # and replace back known keywords to braceless state again
        sp[0] = self.reg.re_unbrace_keywords.sub(r'%\1', sp[0])
        # re-create the line back
        return '#'.join(sp)

    def replace_buildroot(self, line: str) -> str:
        """
        Replace RPM_BUILD_ROOT for buildroot.

        Args:
            line: A string representing a line to process.

        Returns:
            The processed line.
        """
        line = self.reg.re_rpmbuildroot.sub(r'%{buildroot}\2', line)
        line = self.reg.re_rpmbuildroot_quotes.sub(r'%{buildroot}', line)
        return line

    def replace_optflags(self, line: str) -> str:
        """
        Replace RPM_OPT_FLAGS for %{optflags}.

        Args:
            line: A string representing a line to process.

        Returns:
            The processed line.
        """
        # if the optflags is the only thing then also add quotes around it
        line = self.reg.re_optflags_quotes.sub('="%{optflags}"', line)
        line = self.reg.re_optflags.sub('%{optflags}', line)
        return line

    def replace_python_expand(self, line: str) -> str:
        """
        Replace classic python macros with those starting with '$' if it's used with %python_expand macro.

        E.g. with %python_expand one must use "%python_expand %{$python_sitelib}" instead of
        "%python_expand %{python_sitelib}". Known variables: python_sitearch, python_sitelib, python_version,
        python_bin_suffix and python.

        Args:
            line: A string representing a line to process.

        Returns:
            The line with python macros replaced.
        """
        if line.startswith('%python_expand') or line.startswith('%{python_expand'):
            line = self.reg.re_python_expand.sub(r'%{$\1}', line)
            line = self.reg.re_python_interp_expand.sub(r' $\1 ', line)
        return line

    def replace_known_dirs(self, line: str) -> str:
        """
        Replace hardcoded stuff like /usr/share -> %{_datadir}.

        Args:
            line: A string representing a line to process.

        Returns:
            The processed line.
        """
        line = self.reg.re_oldprefix.sub(r'%{_prefix}\1', line)
        line = self.reg.re_prefix.sub(r'%{_prefix}\1', line)
        line = self.reg.re_bindir.sub(r'%{_bindir}\1', line)
        line = self.reg.re_sbindir.sub(r'%{_sbindir}\1', line)
        line = self.reg.re_libexecdir.sub(r'%{_libexecdir}\1', line)
        line = self.reg.re_includedir.sub(r'%{_includedir}\1', line)
        line = self.reg.re_datadir.sub(r'%{_datadir}\1', line)
        line = self.reg.re_mandir.sub(r'%{_mandir}\1', line)
        line = self.reg.re_infodir.sub(r'%{_infodir}\1', line)
        line = self.reg.re_docdir.sub(r'%{_docdir}\1', line)
        line = self.reg.re_initdir.sub(r'%{_initddir}\1', line)
        line = self.reg.re_sysconfdir.sub(r'%{_sysconfdir}\1', line)
        line = self.reg.re_localstatedir.sub(r'%{_localstatedir}\1', line)
        line = self.reg.re_libdir.sub(r'%{_libdir}\2', line)
        line = self.reg.re_initddir.sub(r'%{_initddir}\1', line)

        return line

    def replace_utils(self, line: str) -> str:
        """
        Remove the macro calls for utilities and rather use direct commands (OBS ensures there is only one anyway).

        Args:
            line: A string representing a line to process.

        Returns:
            The line without macros for utilities.
        """
        r = {
            'id_u': 'id -u',
            'ln_s': 'ln -s',
            'lzma': 'xz --format-lzma',
            'mkdir_p': 'mkdir -p',
            'awk': 'gawk',
            'cc': 'gcc',
            'cpp': 'gcc -E',
            'cxx': 'g++',
            'remsh': 'rsh',
        }
        for i in r:
            line = line.replace('%{__' + i + '}', r[i])
            if self.minimal:
                line = line.replace('%__' + i, r[i])

        for i in (
            'aclocal',
            'ar',
            'as',
            'autoconf',
            'autoheader',
            'automake',
            'bzip2',
            'cat',
            'chgrp',
            'chmod',
            'chown',
            'cp',
            'cpio',
            'file',
            'gpg',
            'grep',
            'gzip',
            'id',
            'install',
            'ld',
            'libtoolize',
            'make',
            'mkdir',
            'mv',
            'nm',
            'objcopy',
            'objdump',
            'patch',
            'perl',
            'python',
            'python2',
            'python3',
            'pypy3',
            'ranlib',
            'restorecon',
            'rm',
            'rsh',
            'sed',
            'semodule',
            'ssh',
            'strip',
            'tar',
            'unzip',
            'xz',
        ):
            line = line.replace('%{__' + i + '}', i)
            if self.minimal:
                line = line.replace('%__' + i, i)

        line = self.reg.re_deprecated_egrep_regex.sub(r'grep -E', line)
        line = self.reg.re_deprecated_fgrep_regex.sub(r'grep -F', line)

        return line

    @staticmethod
    def replace_buildservice(line: str) -> str:
        """
        Pretty format the conditions for distribution/version detection.

        Replace %{suse_version} for 0%{?suse_version} and the like.

        Args:
            line: A string representing a line to process.

        Returns:
            The line with formatted version conditions.
        """
        for i in [
            'centos',
            'debian',
            'fedora',
            'mandriva',
            'meego',
            'rhel',
            'sles',
            'suse',
            'ubuntu',
        ]:
            line = line.replace('%{' + i + '_version}', '0%{?' + i + '_version}').replace(
                '00%{', '0%{'
            )
        return line

    def replace_preamble_macros(self, line: str) -> str:
        """
        Replace %{S:0} and %{P:0} for %{SOURCE0} and %{PATCH0}.

        Args:
            line: A string representing a line to process.

        Returns: The processed line.
        """
        line = self.reg.re_ptch.sub(r'%{PATCH\1}', line)
        line = self.reg.re_src.sub(r'%{SOURCE\1}', line)
        return line
