# vim: set ts=4 sw=4 et: coding=UTF-8
import re
from typing import IO, Any

from .rpmregexp import Regexp


class Section:
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
        defined_macros: A set of the macro names the specfile defines with %define or %global.
        condition: A flag representing if we are in the conditional or not.
        _condition_counter: An int for counting in how many (nested) condition we currently are.
        shell_section: A flag indicating whether the section body is a shell script.
    """

    shell_section: bool = False

    def __init__(self, options: dict[str, Any]) -> None:
        """Initialize variables."""
        self.lines: list[str] = []
        self.previous_line: str | None = None
        self.spec: str = options['specfile']
        self.minimal: bool = options['minimal']
        self.no_curlification: bool = options['no_curlification']
        self.reg: Regexp = options['reg']
        self.defined_macros: set[str] = options['defined_macros']
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
        line = line.replace('\xa0', ' ')

        if not line.startswith('#'):
            is_python_module = self.reg.re_python_module.match(line)
            if (
                not self.minimal
                and not self.no_curlification
                # Do not embrace macros inside python_module
                # gh#rpm-software-management/spec-cleaner#321
                and not is_python_module
            ):
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
        # quote bare assignments outside quotes so the flags stay one shell word
        parts = re.split(r'("(?:[^"\\]|\\.)*"?|\'[^\']*\'?)', line)
        parts[::2] = [self.reg.re_optflags_quotes.sub('="%{optflags}"', p) for p in parts[::2]]
        line = ''.join(parts)
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
            line = self.reg.re_python_expand.sub(r'%{$\2}', line)
            line = self.reg.re_python_interp_expand.sub(r'\1$python', line)
        return line

    def replace_known_dirs(self, line: str) -> str:
        """
        Replace hardcoded stuff like /usr/share -> %{_datadir}.

        Args:
            line: A string representing a line to process.

        Returns:
            The processed line.
        """
        # each rewrite only holds while the macros it reads and writes keep their default values
        rules = (
            (self.reg.re_oldprefix, r'%{_prefix}\1', ('_exec_prefix', '_prefix')),
            (self.reg.re_prefix, r'%{_prefix}\1', ('_prefix',)),
            (self.reg.re_bindir, r'%{_bindir}\1', ('_prefix', '_exec_prefix', '_bindir')),
            (self.reg.re_sbindir, r'%{_sbindir}\1', ('_prefix', '_exec_prefix', '_sbindir')),
            (
                self.reg.re_libexecdir,
                r'%{_libexecdir}\1',
                ('_prefix', '_exec_prefix', '_libexecdir'),
            ),
            (self.reg.re_includedir, r'%{_includedir}\1', ('_prefix', '_includedir')),
            (self.reg.re_datadir, r'%{_datadir}\1', ('_prefix', '_datarootdir', '_datadir')),
            (self.reg.re_mandir, r'%{_mandir}\1', ('_datadir', '_mandir')),
            (self.reg.re_infodir, r'%{_infodir}\1', ('_datadir', '_infodir')),
            (self.reg.re_docdir, r'%{_docdir}\1', ('_datadir', '_docdir')),
            (self.reg.re_initdir, r'%{_initddir}\1', ('_sysconfdir', '_initddir')),
            (self.reg.re_sysconfdir, r'%{_sysconfdir}\1', ('_sysconfdir',)),
            (self.reg.re_localstatedir, r'%{_localstatedir}\1', ('_localstatedir',)),
            (
                self.reg.re_ocamlstdlib,
                r'%{ocaml_standard_library}\1',
                ('_prefix', 'ocaml_standard_library'),
            ),
            (self.reg.re_libdir, r'%{_libdir}\2', ('_prefix', '_exec_prefix', '_lib', '_libdir')),
            (self.reg.re_unitdir, r'%{_unitdir}\1', ('_prefix', '_unitdir')),
            (self.reg.re_tmpfilesdir, r'%{_tmpfilesdir}\1', ('_prefix', '_tmpfilesdir')),
            (self.reg.re_sysusersdir, r'%{_sysusersdir}\1', ('_prefix', '_sysusersdir')),
            (self.reg.re_udevrulesdir, r'%{_udevrulesdir}\1', ('_prefix', '_udevrulesdir')),
            (self.reg.re_sysctldir, r'%{_sysctldir}\1', ('_prefix', '_sysctldir')),
            (
                self.reg.re_perlvendorlib,
                r'%{perl_vendorlib}\1',
                ('_prefix', 'perl_version', 'perl_vendorlib'),
            ),
            (self.reg.re_fontsdir, r'%{_fontsdir}\1', ('_datadir', '_fontsdir')),
            (
                self.reg.re_emacssitelispdir,
                r'%{_emacs_sitelispdir}\1',
                ('_datadir', '_emacs_sitelispdir'),
            ),
            (
                self.reg.re_apparmorprofilesdir,
                r'%{apparmor_profilesdir}\1',
                ('_sysconfdir', 'apparmor_profilesdir'),
            ),
            (self.reg.re_nodejssitelib, r'%{nodejs_sitelib}\1', ('_prefix', 'nodejs_sitelib')),
            (self.reg.re_initddir, r'%{_initddir}\1', ('_initrddir', '_initddir')),
        )
        for regexp, replacement, macros in rules:
            if self.defined_macros.isdisjoint(macros):
                line = regexp.sub(replacement, line)

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
            'lzma': 'xz --format=lzma',
            'mkdir_p': 'mkdir -p',
            'awk': 'gawk',
            'cc': 'gcc',
            'cpp': 'gcc -E',
            'cxx': 'g++',
            'remsh': 'rsh',
        }
        # after '#!' the macro is a shebang, which needs the absolute path it expands to
        for i in r:
            if '__' + i in self.defined_macros:
                continue
            line = re.sub(r'(?<!#!)(?<!#! )%\{__' + i + r'\}', r[i], line)
            if self.minimal:
                line = re.sub(r'(?<!#!)(?<!#! )%__' + i + r'\b', r[i], line)

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
            if '__' + i in self.defined_macros:
                continue
            line = re.sub(r'(?<!#!)(?<!#! )%\{__' + i + r'\}', i, line)
            if self.minimal:
                line = re.sub(r'(?<!#!)(?<!#! )%__' + i + r'\b', i, line)

        if self.shell_section:
            line = self.reg.re_deprecated_egrep_regex.sub(r'\1grep -E', line)
            line = self.reg.re_deprecated_fgrep_regex.sub(r'\1grep -F', line)

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
                '00%{?' + i + '_version}', '0%{?' + i + '_version}'
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
