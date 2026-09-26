# vim: set ts=4 sw=4 et: coding=UTF-8

import os.path
import shlex
import subprocess
import sys
import tempfile
from io import StringIO, TextIOWrapper
from typing import IO, Any

from .fileutils import open_stringio_spec
from .rpmbuild import RpmBuild
from .rpmcheck import RpmCheck
from .rpmcopyright import RpmCopyright
from .rpmdescription import RpmDescription
from .rpmexception import RpmExceptionError
from .rpmfiles import RpmFiles
from .rpmhelpers import (
    find_macros_with_arg,
    fix_license,
    load_keywords_whitelist,
    parse_rpm_showrc,
    read_cmake_changes,
    read_group_changes,
    read_licenses_changes,
    read_perl_changes,
    read_pkgconfig_changes,
    read_tex_changes,
)
from .rpminstall import RpmInstall
from .rpmpackage import RpmPackage
from .rpmpreamble import RpmPreamble, RpmPreambleChunk
from .rpmprep import RpmPrep
from .rpmprune import RpmChangelog, RpmClean
from .rpmregexp import Regexp
from .rpmscriplets import RpmScriptlets
from .rpmsection import Section
from .rpmsourcelist import RpmSourceList


class RpmSpecCleaner:
    """
    Class wrapping all sections parser is responsible for.

    It ensures that all sections are checked and accounted for.

    If the section is required and not found it is created with
    blank values as fixme for the spec creator.

    Attributes:
        specfile: A string with the path to the specfile to process.
        fin: An in-memory input stream with the input file data.
        fout: A file object representing output file.
        current_section: A Section object representing current section of spec file.
        skip_run: A bool indicating whether the cleaning of the specfile should be
                 skipped.
        options: A dictionary holding both spec-cleaner commandline arguments and
                 auxiliary options.
        reg: A Regexp object that holds all regexps that will be used in spec-cleaner.
        section_starts: A list of tuples where the first item is regex object
                       representing a start of the specfile section and the second is
                       a corresponding class that should handle it.
        _previous_line: A string holding the previous line of the currently processed
                        specfile.
        _previous_nonempty_line: A string holding a nonempty previous line of the
                                 currently processed specfile.
    """

    specfile: str | None = None
    current_section: Section
    skip_run: bool = False
    _previous_line: str | None = None
    _previous_nonempty_line: str | None = None
    _target: str | None = None

    def __init__(self, options: dict[str, Any]) -> None:
        """
        Initialize and load options into the RpmSpecCleaner obj and run prep methods.

        Args:
            options: A dictionary holding spec-cleaner command line options.
        """
        self.options = options

        # Initialize main license and subpkg option
        self.options['license'] = None
        self.options['subpkglicense'] = False

        # Compile keywords for unbracing
        self.options['unbrace_keywords'] = self._unbrace_keywords()

        # Load all the remaining file operations
        self.options['tex_conversions'] = []
        self.options['pkgconfig_conversions'] = []
        self.options['cmake_conversions'] = []
        self.options['perl_conversions'] = []
        if self.options['tex']:
            self.options['tex_conversions'] = read_tex_changes()
        if self.options['pkgconfig']:
            self.options['pkgconfig_conversions'] = read_pkgconfig_changes()
        if self.options['cmake']:
            self.options['cmake_conversions'] = read_cmake_changes()
        if self.options['perl']:
            self.options['perl_conversions'] = read_perl_changes()
        self.options['license_conversions'] = read_licenses_changes()
        if self.options['remove_groups']:
            self.options['allowed_groups'] = None
        else:
            self.options['allowed_groups'] = read_group_changes()
        self.options['reg'] = Regexp(self.options['unbrace_keywords'])

        # If gvim is used for the diff then run it in foreground mode
        if self.options['diff_prog'].startswith('gvim') and ' -f' not in self.options['diff_prog']:
            self.options['diff_prog'] += ' -f'

        self.reg = self.options['reg']
        self.fin = open_stringio_spec(self.options['specfile'])

        # Section starts detection
        self.section_starts = [
            (self.reg.re_spec_package, RpmPackage),
            (self.reg.re_spec_description, RpmDescription),
            (self.reg.re_spec_sourcelist, RpmSourceList),
            (self.reg.re_spec_patchlist, RpmSourceList),
            (self.reg.re_spec_prep, RpmPrep),
            (self.reg.re_spec_generate_buildrequires, RpmBuild),
            (self.reg.re_spec_conf, RpmBuild),
            (self.reg.re_spec_build, RpmBuild),
            (self.reg.re_spec_install, RpmInstall),
            (self.reg.re_spec_clean, RpmClean),
            (self.reg.re_spec_check, RpmCheck),
            (self.reg.re_spec_scriptlets, RpmScriptlets),
            (self.reg.re_spec_triggers, RpmScriptlets),
            (self.reg.re_spec_files, RpmFiles),
            (self.reg.re_spec_changelog, RpmChangelog),
        ]

        # Find all the present licenses
        self._load_licenses()

        # Determine if we need to skip the spec ('#nospeccleaner' tag)
        self._find_skip_parser()

        # Detect %lang_package macro usage for redundant Recommends pruning (#273)
        self._find_lang_package()

        self._find_defined_macros()

        self._find_bare_patch()

        # Set what will be the output of the cleaning
        self._select_mode()

    def _select_mode(self) -> None:
        """
        Set up what will be the output of the cleaning process.

        Based on the options given to the commandline possible options are: output file, inline or a diff program
        showing differences.
        """
        self.fout: IO[Any]
        # buffer file output so a run failing while cleaning leaves the file untouched
        if self.options['output']:
            self._target = self.options['output']
            self.fout = StringIO()
        elif self.options['inline']:
            self._target = self.options['specfile']
            self.fout = StringIO()
        elif self.options['diff']:
            self.fout = tempfile.NamedTemporaryFile(
                mode='w+',
                encoding='utf-8',
                prefix=os.path.split(self.options['specfile'])[-1] + '.',
                suffix='.spec',
            )
        else:
            # spec files are UTF-8 whatever the locale charset is
            if isinstance(sys.stdout, TextIOWrapper):
                sys.stdout.reconfigure(encoding='utf-8')
            self.fout = sys.stdout

    def _unbrace_keywords(self) -> list[str]:
        """
        Create a list of keywords that shouldn't be in the curly brackets.

        It searches for keywords in the whitelist file, global macro functions in 'rpm --showrc' and macro functions
        in the specfile.

        Returns:
            A list of such keywords.
        """
        keywords = load_keywords_whitelist()
        global_macrofuncs = parse_rpm_showrc()
        spec_macrofuncs = find_macros_with_arg(self.options['specfile'])
        return keywords + global_macrofuncs + spec_macrofuncs

    def _find_skip_parser(self) -> None:
        """
        Search the specfile for the user defined '#nospeccleaner' tag.

        This tag means that specfile shouldn't be cleaned. If the tag is found then
        skip_run member is set to True, else it's False.
        """
        for line in self.fin:
            if self.reg.re_skipcleaner.match(line):
                self.skip_run = True
                break
        self.fin.seek(0)

    def _find_lang_package(self) -> None:
        """
        Collect the -lang subpackages generated by the %lang_package macro.

        The macro generates Supplements for the -lang subpackage, making a
        manual Recommends on it redundant (#273).
        """
        self.options['lang_package'] = set()
        main_name = None
        for line in self.fin:
            match = self.reg.re_name.match(line)
            if match and main_name is None:
                main_name = self.reg.re_macro_spelling.sub(r'%{\1}', match.group(1))
            if self.reg.re_lang_package.match(line):
                match = self.reg.re_lang_package_name.search(line)
                name = match.group(1) if match else '%{name}'
                name = self.reg.re_macro_spelling.sub(r'%{\1}', name)
                # -n with the main package's Name still generates its own lang package
                if name == main_name:
                    name = '%{name}'
                self.options['lang_package'].add(f'{name}-lang')
        self.fin.seek(0)

    def _find_defined_macros(self) -> None:
        """
        Collect the names of the macros the specfile defines with %define or %global.

        The path and utility replacements must not assume rpm's default values for them.
        """
        self.options['defined_macros'] = set()
        for line in self.fin:
            match = self.reg.re_macro_definition.match(line.lstrip())
            if match:
                self.options['defined_macros'].add(match.group(1))
        self.fin.seek(0)

    def _find_bare_patch(self) -> None:
        """
        Decide whether the first unnumbered Patch tag must be numbered 0.

        The %prep cleaning turns a bare %patch into '%patch -P 0', so without an
        explicit Patch0 the unnumbered Patch it applied has to become Patch0.
        """
        bare_patch = False
        has_patch0 = False
        for line in self.fin:
            line = line.rstrip()
            match = self.reg.re_patch.match(line)
            if match and not match.group(1) and match.group(2) and int(match.group(2)) == 0:
                has_patch0 = True
            is_patch = line.startswith('%patch ') or line == '%patch'
            if is_patch and not RpmPrep._has_patch_number(line):
                bare_patch = True
        self.options['rename_unnumbered_patch'] = (
            not self.options['minimal'] and bare_patch and not has_patch0
        )
        self.fin.seek(0)

    def _load_licenses(self) -> None:
        """
        Detect all present licenses in the specfile and load them into 'options' member.

        If we have more than one then put license to the each subpkg.
        """
        licenses: list[str] = []
        depth = 0
        first_conditional = False
        for line in self.fin:
            if self.reg.re_if.match(line):
                depth += 1
            elif self.reg.re_endif.match(line):
                depth -= 1
            elif self.reg.re_license.match(line):
                line = line.rstrip('\n')
                line = line.rstrip('\r')
                line = line.rstrip()
                match = self.reg.re_license.match(line)
                value = fix_license(match.groups()[-1], self.options['license_conversions'])
                if not licenses:
                    first_conditional = depth > 0
                if value not in licenses:
                    licenses.append(value)
        if len(licenses) > 1:
            self.options['subpkglicense'] = True
            # put first license as placeholder where missing, unless only some builds use it
            if not first_conditional:
                self.options['license'] = licenses[0]
        self.fin.seek(0)

    def _detect_preamble_section(self, line: str) -> bool:
        """
        Detect if the line starts a preamble or not.

        Args:
            line: A string representing a line to process.

        Returns:
            True if it's a preamble, False otherwise.
        """
        # This is seriously ugly but can't think of cleaner way FIXME
        if not isinstance(self.current_section, (RpmPreamble, RpmPackage)):
            if any(re.match(line) for re in [self.reg.re_bcond_with, self.reg.re_debugpkg]):
                return True

            # We can have locally defined variables in phases
            if not isinstance(self.current_section, (RpmInstall, RpmCheck, RpmBuild, RpmPrep)) and (
                self.reg.re_define.match(line) or self.reg.re_global.match(line)
            ):
                # a one-line define that continues a scriptlet or file list body is local to it
                return not (
                    isinstance(self.current_section, (RpmScriptlets, RpmFiles))
                    and self._previous_line
                    and not line.endswith('\\')
                    and line.count('{') == line.count('}')
                )
        return False

    def _detect_condition_change(self, line: str) -> bool:
        """
        Detect if the line contains a condition change.

        (e.g. '%endif', '%else' or the end of the code block)

        Args:
            line: A string representing a line to process.

        Returns:
             True if a condition change was found, False otherwise.
        """
        if any(
            re.match(line)
            for re in [self.reg.re_endif, self.reg.re_else_elif, self.reg.re_endcodeblock]
        ):
            return True
        return False

    def _detect_new_section(self, line: str) -> type[Section] | None:
        """
        Detect if the line contains a new section (and which) or not.

        Args:
            line: A string representing a line to process.

        Returns:
            A Section (or a subclass) object that was detected.
            None if we are staying in the same section or if we have a multiline value from preamble.
        """
        if self._is_multiline_active():
            return None

        if self._is_clean_codeblock_end(line):
            return None

        breakout = self._check_condition_breakout(line)
        if breakout:
            return breakout

        section_start = self._check_section_start(line)
        if section_start:
            return section_start

        copyright_transition = self._check_copyright_transition(line)
        if copyright_transition:
            return copyright_transition

        if self._detect_preamble_section(line):
            return RpmPreambleChunk

        if self._is_clean_section_end(line):
            return Section

        # we are staying in the section
        return None

    def _is_multiline_active(self) -> bool:
        """Check if the current section has an active multiline value. Return True if so."""
        # mypy: we need to ignore type check here because mypy cannot detect that we are checking the existence of
        # the 'multiline' attribute before accessing it
        return hasattr(self.current_section, 'multiline') and self.current_section.multiline  # type: ignore

    def _is_clean_codeblock_end(self, line: str) -> bool:
        """Check if the line ends a codeblock in the dropped %clean body. Return True if so."""
        # comment markers opened in the dropped %clean body wrap nothing
        return bool(
            isinstance(self.current_section, RpmClean)
            and self.current_section.codeblocks
            and self.reg.re_endcodeblock.match(line)
        )

    def _check_condition_breakout(self, line: str) -> type[Section] | None:
        """Check if we need to break out for a condition from global space. Return Section if so, None otherwise."""
        # Detect if we match condition and that is from global space
        # Ie like in the optional packages where if is before class definition
        # For the "if" we need to detect it more smartly:
        #   check if the current line is starting new section, and if so
        #   if previous non-empty-uncommented line was starting the condition
        # we end up the condition section in preamble (if applicable) and
        # proceed to output
        if self._detect_condition_change(line) or (
            type(self.current_section) is Section
            and (self.reg.re_if.match(line) or self.reg.re_codeblock.match(line))
        ):
            if not hasattr(self.current_section, 'condition') or (
                hasattr(self.current_section, 'condition') and not self.current_section.condition
            ):
                # If we have to break out we go ahead with small class
                # which just print the one evil line
                return Section
        return None

    def _check_section_start(self, line: str) -> type[Section] | None:
        """Check if the line starts a specific section. Return the section class if so, None otherwise."""
        # try to verify if we start some specific section
        for regexp, newclass in self.section_starts:
            if regexp.match(line):
                # check if we are in if conditional and act accordingly if we
                # change sections
                if hasattr(self.current_section, 'condition') and self.current_section.condition:
                    self.current_section.condition = False
                    if hasattr(self.current_section, 'end_subparagraph'):
                        # mypy: we need to ignore type check here because mypy cannot detect that we are checking the
                        # existence of the 'end_subparagraph' attribute before accessing it
                        # close every open nested level, not just the innermost one
                        while self.current_section._oldstore:  # type: ignore
                            self.current_section.end_subparagraph(unclosed=True)  # type: ignore
                return newclass
        return None

    def _check_copyright_transition(self, line: str) -> type[Section] | None:
        """Check if we transition from copyright to preamble. Return RpmPreamble if so, None otherwise."""
        # if we still are here and we are just doing copyright
        # and we are not on commented line anymore, just jump to Preamble
        if isinstance(self.current_section, RpmCopyright):
            if not self.reg.re_comment.match(line):
                return RpmPreamble
            # an OBS '#!' directive after the header's blank line starts the preamble
            if (
                self.current_section.suse_copyright
                and self.current_section.header_seen
                and line.startswith('#!')
                and self._previous_line == ''
            ):
                return RpmPreamble
            # if we got two empty lines then the copyright also ended
            if self._previous_line == '' and line == '':
                self.current_section.add(line)
                return RpmPreamble
        return None

    def _is_clean_section_end(self, line: str) -> bool:
        """Check if we end the %clean section on a blank line followed by non-command. Return True if so."""
        # If we are in clean section and a blank line is followed by
        # anything but a command we need to stop deleting
        # This avoids deleting %if before %files section
        return (
            isinstance(self.current_section, RpmClean)
            and self.current_section.previous_line == ''
            and line.lstrip().startswith(('%', '#'))
            and not line.lstrip().startswith(('%__', '%{__'))
        )

    def _check_for_newline(self, detected_class: type[Section] | None, line: str) -> bool:
        """
        Check if we want newline or not after the end of section detected.

        Args:
            detected_class: A Section class (or a subclass) representing section that needs to be checked.
            line: A string representing a line to process.

        Returns: True if we want a newline, False otherwise.
        """
        # We don't want to print newlines before %else and %endif
        if detected_class == Section and self._detect_condition_change(line):
            return False
        else:
            # We also do not want to print newline if at the end of the
            # previous section we actually had a commentary, ie comment above
            # new section
            if self._previous_line and self._previous_line.startswith('#'):
                return False
            else:
                return True

    def run(self) -> None:
        """
        Run the main spec-cleaner method.

        Raises:
            RpmExceptionError if a diff program can't be executed.
        """
        # If we are skipping the specfile we should do nothing
        if self.skip_run:
            sys.stderr.write(
                ".spec file {} is not being processed due to definiton of 'nospeccleaner'\n".format(
                    self.options['specfile']
                )
            )
            for line in self.fin:
                self.fout.write(line)
            self.fout.flush()
            self._write_target()
            return

        # We always start with Copyright
        self.current_section = RpmCopyright(self.options)

        # FIXME: we need to store the content locally and then reorder
        #        to maintain the specs all the same (eg somebody put
        #        filelist to the top).
        for line in self.fin:
            # Remove newlines to make it easier to parse things
            line = line.rstrip('\n')
            line = line.rstrip('\r')

            new_class = self._detect_new_section(line)
            # Following line is debug output with class info
            # USE: 'spec-cleaner file > /dev/null' to see the stderr output
            # sys.stderr.write("class: '{0}' line: '{1}'\n".format(new_class, line))
            if new_class:
                self.current_section.output(
                    self.fout,
                    self._check_for_newline(new_class, line),
                    new_class.__name__,
                )
                # start new class
                self.current_section = new_class(self.options)
                # skip empty line adding if we are switching sections
                if self._previous_line == '' and line == '':
                    continue

            self.current_section.add(line)
            # keep %clean lines out of the previous-line tracking
            if isinstance(self.current_section, RpmClean):
                continue
            self._previous_line = line
            if line != '' and not line.startswith('#'):
                self._previous_nonempty_line = line

        # no need to not output newline at the end even for minimal -> no condition
        self.current_section.output(self.fout)
        # add changelog at the end of the file
        if (
            not isinstance(self.current_section, RpmChangelog)
            and self._previous_nonempty_line != '%changelog'
        ):
            self.fout.write('%changelog\n')
        self.fout.flush()
        self._write_target()

        # if the '--diff' option was used, run the diff program
        if self.options['diff']:
            cmd = shlex.split(self.options['diff_prog']) + [
                self.options['specfile'],
                self.fout.name,
            ]
            try:
                subprocess.call(cmd, shell=False)
            except OSError as error:
                prog = self.options['diff_prog'].split()[0]
                raise RpmExceptionError(f'Could not execute {prog} ({error.strerror})') from error

    def _write_target(self) -> None:
        """Write the buffered output to the output file or back to the spec."""
        if self._target and isinstance(self.fout, StringIO):
            with open(self._target, 'w', encoding='utf-8') as f:
                f.write(self.fout.getvalue())

    def __del__(self) -> None:
        """Close the input and output files."""
        if hasattr(self, 'fin'):
            self.fin.close()
        if hasattr(self, 'fout') and self.fout is not sys.stdout:
            self.fout.close()
